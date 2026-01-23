import subprocess
import time
import os
import shutil
import psutil

class BenchmarkRunner:
    def __init__(self, config):
        self.config = config



    def run_benchmark(self, language, source_path, iterations=5, on_status=None):
        def log(msg):
            if on_status:
                on_status(msg)
            else:
                print(msg)

        lang_config = self.config.get('languages', {}).get(language)
        if not lang_config:
            raise ValueError(f"Unknown language: {language}")

        # Prepare output binary path if needed
        bin_dir = os.path.join(os.path.dirname(source_path), 'bin')
        os.makedirs(bin_dir, exist_ok=True)
        bin_name = f"runner_{language}"
        bin_path = os.path.join(bin_dir, bin_name)

        # Compile if necessary
        try:
            compile_cmd_tpl = lang_config.get('compile')
            if compile_cmd_tpl:
                cmd = compile_cmd_tpl.format(source=source_path, out=bin_path)
                log(f"Compiling...")
                # For Java and C#, we need to run compile in the source directory
                cwd = os.path.dirname(source_path) if language in ['java', 'csharp'] else None
                subprocess.check_call(cmd, shell=True, cwd=cwd)
            else:
                # No compilation needed
                pass
        except subprocess.CalledProcessError as e:
            log(f"[red]Compilation failed[/red]: {e}")
            return None

        run_cmd_tpl = lang_config.get('run')
        # If compiled, use bin_path, else use source_path
        cmd = run_cmd_tpl.format(source=source_path, out=bin_path)

        times = []
        max_mems = []

        for i in range(iterations):
            log(f"Running iteration {i+1}/{iterations}...")
            start = time.time()
            try:
                # Always run in the source directory for consistency
                cwd = os.path.dirname(source_path)
                
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, cwd=cwd)
                
                # Monitor memory
                peak_mem = 0
                try:
                    p = psutil.Process(process.pid)
                    while process.poll() is None:
                        try:
                            # rss is Resident Set Size (RAM usage)
                            mem_info = p.memory_info()
                            peak_mem = max(peak_mem, mem_info.rss)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            break
                        time.sleep(0.005) # Poll every 5ms
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    # Process finished too quickly
                    pass
                
                process.wait() # Ensure process is done
                
                if process.returncode != 0:
                    raise subprocess.CalledProcessError(process.returncode, cmd)

                duration = time.time() - start
                times.append(duration)
                max_mems.append(peak_mem)
                
            except subprocess.CalledProcessError as e:
                log(f"[red]Runtime error[/red]: {e}")
                return None

        # simple stats
        # simple stats
        avg_mem_usage = sum(max_mems) / len(max_mems) if max_mems else 0
        return {
            'mean': sum(times) / len(times),
            'min': min(times),
            'max': max(times),
            'count': len(times),
            'avg_memory': avg_mem_usage,
            'max_memory': max(max_mems) if max_mems else 0
        }
