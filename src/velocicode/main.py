import argparse
import yaml
import os
import sys
from glob import glob
import shutil
from .runner import BenchmarkRunner
from .reporter import print_table
from .system_info import get_system_info
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

console = Console()

def check_dependencies(config, verbose=True):
    if verbose:
        rprint(Panel("Checking System Dependencies", style="bold blue"))
    
    languages = config.get('languages', {})
    valid_langs = set()
    missing_langs = set()
    
    for lang, cfg in languages.items():
        # Determine the command to check
        # If 'compile' exists, check the compiler. Else check 'run'.
        cmd_str = cfg.get('compile') or cfg.get('run')
        if not cmd_str:
            if verbose:
                rprint(f"[yellow]WARN[/yellow] {lang}: No command defined")
            continue
            
        # simpler parsing: assume command is the first word
        program = cmd_str.split()[0]
        
        path = shutil.which(program)
        if path:
            if verbose:
                rprint(f"[green]✔[/green] {lang:<12} (Found: [cyan]{program}[/cyan])")
            valid_langs.add(lang)
        else:
            if verbose:
                rprint(f"[red]✘[/red] {lang:<12} (Missing: [bold]{program}[/bold])")
                if lang == 'java' and shutil.which('java'):
                    rprint(f"  [dim]Tip: You have 'java' but not 'javac'. Install the JDK package (e.g. java-latest-openjdk-devel).[/dim]")
            missing_langs.add(lang)
            
    return valid_langs, missing_langs


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
    parser = argparse.ArgumentParser(description="Velocicode - Programming Language Speed Benchmark Tool")
    parser.add_argument("action", choices=["run", "list", "check"], help="Action to perform")
    parser.add_argument("--filter-algo", help="Filter by specific algorithm name")
    parser.add_argument("--filter-lang", help="Filter by specific languages (comma separated)")
    parser.add_argument("--iter", type=int, default=5, help="Number of iterations per benchmark")
    parser.add_argument("--json", help="Export results to a JSON file")
    parser.add_argument("--html", help="Export results to an interactive HTML report")
    
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
        # 1. Display System Info
        sys_info = get_system_info()
        info_text = f"""
[bold]OS:[/bold]   {sys_info['os']}
[bold]CPU:[/bold]  {sys_info['cpu']}
[bold]Arch:[/bold] {sys_info['arch']}
[bold]RAM:[/bold]  {sys_info['ram']}
"""
        rprint(Panel(info_text.strip(), title="System Information", border_style="green"))

        # 2. Check Dependencies
        valid_langs, missing_langs = check_dependencies(config, verbose=False)
        
        if missing_langs:
            rprint(f"[yellow]Warning: The following languages are missing:[/yellow] [bold]{', '.join(missing_langs)}[/bold]")
            if not Confirm.ask("Do you want to continue running valid languages only?"):
                rprint("[red]Aborted.[/red]")
                return

        base_dir = os.path.join(get_base_dir(), "benchmarks")
        
        # Collect all tasks first
        tasks_to_run = []
        for algo in algos:
            algo_dir = os.path.join(base_dir, algo)
            lang_dirs = [d for d in os.listdir(algo_dir) if os.path.isdir(os.path.join(algo_dir, d)) and d != 'bin']
            
            for lang in lang_dirs:
                if target_langs and lang not in target_langs:
                    continue
                
                # SKIP if missing
                if lang in missing_langs:
                    continue
                
                ext_map = {
                    'python': 'main.py',
                    'cpp': 'main.cpp',
                    'rust': 'main.rs',
                    'go': 'main.go',
                    'javascript': 'main.js',
                    'java': 'Main.java',
                    'csharp': 'Program.cs'
                }
                expected_file = ext_map.get(lang)
                if not expected_file:
                    continue
                full_path = os.path.join(algo_dir, lang, expected_file)
                if not os.path.exists(full_path):
                    continue
                tasks_to_run.append((algo, lang, full_path))

        if not tasks_to_run:
            rprint("[yellow]No benchmarks found to run.[/yellow]")
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            for algo, lang, full_path in tasks_to_run:
                # Initial task description
                desc_tpl = f"[bold cyan]{algo}[/bold cyan] ([magenta]{lang}[/magenta])"
                task_id = progress.add_task(f"{desc_tpl}: Starting...", total=None)
                
                def update_status(msg):
                    # update progress description
                    progress.update(task_id, description=f"{desc_tpl}: {msg}")
                
                stats = runner.run_benchmark(lang, full_path, iterations=args.iter, on_status=update_status)
                progress.remove_task(task_id)
                
                if stats:
                    results.append({
                        'benchmark': algo,
                        'language': lang,
                        **stats
                    })

        print_table(results)
        
        if args.json:
            import json
            with open(args.json, 'w') as f:
                json.dump(results, f, indent=2)
            rprint(f"[green]JSON results exported to:[/green] {args.json}")
            
        if args.html:
            from .report_generator import generate_html_report
            generate_html_report(results, args.html)
            rprint(f"[green]HTML report generated at:[/green] {args.html}")

def interactive_menu():
    rprint(Panel.fit("[bold cyan]Velocicode[/bold cyan]\n[dim]High-Performance Benchmark CLI[/dim]", title="Welcome", border_style="blue"))
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
        print("\n[bold]Available Algorithms:[/bold]")
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
