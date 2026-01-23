import platform
import psutil
import cpuinfo

def get_system_info():
    """
    Returns a dictionary containing system information.
    """
    cpu_info = cpuinfo.get_cpu_info()
    cpu_model = cpu_info.get('brand_raw', 'Unknown CPU')
    arch = platform.machine().lower()
    if arch in ['aarch64', 'arm64']:
        arch = 'ARM64'
    elif arch in ['x86_64', 'amd64']:
        arch = 'x86_64'
    else:
        arch = platform.machine()
    
    ram_bytes = psutil.virtual_memory().total
    ram_gb = ram_bytes / (1024**3)
    
    os_info = f"{platform.system()} {platform.release()}"
    
    return {
        "os": os_info,
        "cpu": cpu_model,
        "arch": arch,
        "ram": f"{ram_gb:.1f} GB"
    }
