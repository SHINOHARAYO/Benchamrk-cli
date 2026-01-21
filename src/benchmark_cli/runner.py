import subprocess
import time
import os
import shutil

class BenchmarkRunner:
    def __init__(self, config):
        self.config = config

    def compile(self, language, source_path, output_path):
        lang_config = self.config.get('languages', {}).get(language)
        if not lang_config:
            raise ValueError(f"Unknown language: {language}")

        compile_cmd_tpl = lang_config.get('compile')
        if compile_cmd_tpl:
            cmd = compile_cmd_tpl.format(source=source_path, out=output_path)
            print(f"[{language}] Compiling: {cmd}")
            subprocess.check_call(cmd, shell=True)
            return output_path
        return None

    def run_benchmark(self, language, source_path, iterations=5):
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
            self.compile(language, source_path, bin_path)
        except subprocess.CalledProcessError as e:
            print(f"[{language}] Compilation failed: {e}")
            return None

        run_cmd_tpl = lang_config.get('run')
        # If compiled, use bin_path, else use source_path
        # The config.yaml logic expects {out} if compiled, or {source} if interpreted.
        # We need to map correctly.
        
        # Check if 'compile' existed to decide whether to pass {out} or {source}
        # Actually easier to just provide both and let the template ignore one.
        cmd = run_cmd_tpl.format(source=source_path, out=bin_path)

        times = []
        for i in range(iterations):
            print(f"[{language}] Running iteration {i+1}/{iterations}...")
            start = time.time()
            try:
                subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL)
                duration = time.time() - start
                times.append(duration)
            except subprocess.CalledProcessError as e:
                print(f"[{language}] Runtime error: {e}")
                return None

        # simple stats
        return {
            'mean': sum(times) / len(times),
            'min': min(times),
            'max': max(times),
            'count': len(times)
        }
