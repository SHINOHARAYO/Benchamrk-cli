from rich import print
from rich.table import Table
from rich.console import Console

def print_table(results):
    if not results:
        print("[yellow]No results to display[/yellow]")
        return
    
    console = Console()
    
    # 1. Group by Benchmark
    grouped = {}
    for r in results:
        bench_name = r['benchmark']
        if bench_name not in grouped:
            grouped[bench_name] = []
        grouped[bench_name].append(r)
        
    # 2. Process each group
    for bench_name, group_results in grouped.items():
        # Sort by mean time (fastest first)
        group_results.sort(key=lambda x: x['mean'])
        
        # Determine baseline (fastest)
        if not group_results:
            continue
            
        fastest_time = group_results[0]['mean']
        
        # Create Table
        table = Table(
            title=f"Benchmark: [bold cyan]{bench_name}[/bold cyan]",
            show_header=True,
            header_style="bold white",
            border_style="blue",
            expand=True
        )
        
        table.add_column("Rank", style="bold yellow", justify="center", width=4)
        table.add_column("Language", style="magenta", width=12)
        table.add_column("Time (s)", justify="right")
        table.add_column("Relative", justify="right")
        table.add_column("Min (s)", style="dim", justify="right")
        table.add_column("Max (s)", style="dim", justify="right")
        table.add_column("Max RAM", style="cyan", justify="right")

        for i, r in enumerate(group_results):
            # Rank
            rank_display = str(i + 1)
            if i == 0:
                rank_display = "🥇"
            elif i == 1:
                rank_display = "🥈"
            elif i == 2:
                rank_display = "🥉"
            
            # Relative Speed
            rel_speed = r['mean'] / fastest_time
            rel_str = f"{rel_speed:.2f}x"
            
            # Colorize Relative Speed
            if rel_speed < 1.05:
                rel_style = "[green]"
            elif rel_speed < 5.0:
                rel_style = "[yellow]"
            else:
                rel_style = "[red]"
            
            # Memory Formatting
            mem_bytes = r.get('max_memory', 0)
            if mem_bytes > 1024 * 1024:
                mem_str = f"{mem_bytes / (1024*1024):.1f} MB"
            elif mem_bytes > 1024:
                mem_str = f"{mem_bytes / 1024:.1f} KB"
            else:
                mem_str = f"{mem_bytes} B"
            
            table.add_row(
                rank_display,
                r['language'],
                f"{r['mean']:.4f}",
                f"{rel_style}{rel_str}[/]",
                f"{r['min']:.4f}",
                f"{r['max']:.4f}",
                mem_str
            )
            
        console.print(table)
        console.print("") # Newline between tables
