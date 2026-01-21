import subprocess
import time
import os
import shutil

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
        for i in range(iterations):
            log(f"Running iteration {i+1}/{iterations}...")
            start = time.time()
            try:
                # For Java and C#, we need to run in the source directory
                cwd = os.path.dirname(source_path) if language in ['java', 'csharp'] else None
                subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL, cwd=cwd)
                duration = time.time() - start
                times.append(duration)
            except subprocess.CalledProcessError as e:
                log(f"[red]Runtime error[/red]: {e}")
                return None

        # simple stats
        return {
            'mean': sum(times) / len(times),
            'min': min(times),
            'max': max(times),
            'count': len(times)
        }
