import asyncio
import sys
import time
import argparse

async def io_task(duration):
    # Simulate I/O waiting
    await asyncio.sleep(duration)

async def main_async(n):
    tasks = []
    # Create N tasks
    # To make it more interesting, let's have them actually do something 
    # slightly distinct or just massive concurrency?
    # Massive concurrency is the goal.
    
    # We want to measure the overhead of scheduling.
    # So we spawn N tasks that wait for a bit.
    io_duration = 0.01 # 10ms wait
    
    # Using 0.01s wait for 10,000 tasks -> minimal total wait if parallel
    for _ in range(n):
        tasks.append(io_task(io_duration))
        
    await asyncio.gather(*tasks)

def main():
    try:
        # Default to larger N for async tests because they are fast
        n = 1000 if len(sys.argv) <= 1 else int(sys.argv[1])
        # If N is small (passed by runner default 5?), we should scale it?
        # Runner passes 'iterations' as loop count, but here N usually means "workload size".
        # Runner logic: run_benchmark(..., iterations=5).
        # It calls the binary.
        # Arguments passed to binary: currently main.py just accepts one arg.
        # User config for 'iterations' usually defaults to 5.
        # The arguments passed to the process are controlled by `runner.py` calling `run_cmd.format(...)`.
        # `runner.py` does NOT pass arguments by default unless configured?
        # Wait, `runner.py` loops `iterations` times and calls `cmd`.
        # `cmd` usually includes `{source}`.
        # Where does `N` (workload size) come from?
        # In `fibonacci`, it's hardcoded or passed via argv if supported?
        # Let's check `fibonacci/python/main.py`.
        pass
    except ValueError:
        n = 1000

    # Actually, the runner loops the EXECUTION.
    # The workload size N is usually internal or passed as arg.
    # For `fibonacci`, it's usually fixed (e.g. 35).
    # For `async_io`, we should probably fix the task count to something significant, e.g., 10,000.
    # And allow argv override.
    
    # If sys.argv[1] is provided, use it as task count.
    
    loop_count = 10000 
    if len(sys.argv) > 1:
        try:
            loop_count = int(sys.argv[1])
        except:
             pass

    start_time = time.time()
    asyncio.run(main_async(loop_count))
    duration = time.time() - start_time
    
    # Output check?
    # No output needed for runner, just time.
    
if __name__ == "__main__":
    main()
