import argparse
import yaml
import os
import sys
from glob import glob
import shutil
from .runner import BenchmarkRunner
from .reporter import print_table

def check_dependencies(config):
    print("Checking System Dependencies:")
    languages = config.get('languages', {})
    
    for lang, cfg in languages.items():
        # Determine the command to check
        # If 'compile' exists, check the compiler. Else check 'run'.
        cmd_str = cfg.get('compile') or cfg.get('run')
        if not cmd_str:
            print(f"[UNKNOWN] {lang}: No command defined")
            continue
            
        # simpler parsing: assume command is the first word
        program = cmd_str.split()[0]
        
        path = shutil.which(program)
        if path:
            print(f"[PASS] {lang:<12} (Found: {program})")
        else:
            print(f"[FAIL] {lang:<12} (Missing: {program})")


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))

def load_config():
    path = os.path.join(get_base_dir(), "config.yaml")
    if not os.path.exists(path):
        print(f"Config file not found: {path}")
        sys.exit(1)
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def discover_benchmarks():
    base_dir = os.path.join(get_base_dir(), "benchmarks")
    # Structure: benchmarks/<algo>/<lang>/<file>
    # We want to find all <algo> directories
    if not os.path.exists(base_dir):
        return []
    return [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

def main():
    parser = argparse.ArgumentParser(description="Programming Language Speed Benchmark Tool")
    parser.add_argument("action", choices=["run", "list", "check"], help="Action to perform")
    parser.add_argument("--filter-algo", help="Filter by specific algorithm name")
    parser.add_argument("--filter-lang", help="Filter by specific languages (comma separated)")
    parser.add_argument("--iter", type=int, default=5, help="Number of iterations per benchmark")
    
    args = parser.parse_args()
    
    config = load_config()
    
    if args.action == "check":
        check_dependencies(config)
        return

    runner = BenchmarkRunner(config)
    
    algos = discover_benchmarks()
    if args.filter_algo:
        algos = [a for a in algos if a == args.filter_algo]
        
    target_langs = None
    if args.filter_lang:
        target_langs = args.filter_lang.split(',')

    results = []

    if args.action == "list":
        print("Available benchmarks:")
        for a in algos:
            print(f" - {a}")
        return

    if args.action == "run":
        base_dir = os.path.join(get_base_dir(), "benchmarks")
        for algo in algos:
            algo_dir = os.path.join(base_dir, algo)
            # Find language directories
            lang_dirs = [d for d in os.listdir(algo_dir) if os.path.isdir(os.path.join(algo_dir, d)) and d != 'bin']
            
            for lang in lang_dirs:
                if target_langs and lang not in target_langs:
                    continue
                
                # Assume main entry file exists. Logic could be improved here.
                # Try main.py, main.cpp, main.rs, main.go, main.js
                # Or just look for any file.
                # For simplicity, let's look for known extensions based on config
                
                src_file = None
                # naive helper mapping
                ext_map = {
                    'python': 'main.py',
                    'cpp': 'main.cpp',
                    'rust': 'main.rs',
                    'go': 'main.go',
                    'javascript': 'main.js'
                }
                
                expected_file = ext_map.get(lang)
                if not expected_file:
                    print(f"Skipping unknown structure for {lang} in {algo}")
                    continue
                    
                full_path = os.path.join(algo_dir, lang, expected_file)
                if not os.path.exists(full_path):
                    print(f"Source file missing: {full_path}")
                    continue

                print(f"Running {algo} - {lang}...")
                stats = runner.run_benchmark(lang, full_path, iterations=args.iter)
                if stats:
                    results.append({
                        'benchmark': algo,
                        'language': lang,
                        **stats
                    })

        print("\n\n=== Final Results ===")
        print_table(results)

def interactive_menu():
    print("\nWelcome to the Benchmark Tool!")
    print("1. Run All Benchmarks")
    print("2. Run Specific Algorithm")
    print("3. Run Specific Language")
    print("4. Check Dependencies")
    print("5. Exit")
    
    choice = input("Enter choice: ").strip()
    
    if choice == '1':
        return ["run"]
    elif choice == '2':
        algos = discover_benchmarks()
        print("\nAvailable Algorithms:")
        for i, a in enumerate(algos):
            print(f"{i+1}. {a}")
        idx = input("Select algorithm number: ").strip()
        try:
            algo = algos[int(idx)-1]
            return ["run", "--filter-algo", algo]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return interactive_menu()
    elif choice == '3':
        lang = input("Enter language (e.g. python, cpp): ").strip()
        return ["run", "--filter-lang", lang]
    elif choice == '4':
        return ["check"]
    elif choice == '5':
        sys.exit(0)
    else:
        print("Invalid choice.")
        return interactive_menu()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        args = interactive_menu()
        # Hack: modify sys.argv so argparse parses our generated args
        sys.argv = [sys.argv[0]] + args
        main()
    else:
        main()
