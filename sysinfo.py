import platform
import socket
import uuid
import psutil

def get_size(bytes, suffix="B"):
    """Перевод байт в человекочитаемый формат"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def collect_info():
    print("="*40, "System Information", "="*40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    
    print("="*40, "CPU Info", "="*40)
    print(f"Physical cores: {psutil.cpu_count(logical=False)}")
    print(f"Total cores: {psutil.cpu_count(logical=True)}")
    
    print("="*40, "Memory Information", "="*40)
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    
    print("="*40, "Disk Information", "="*40)
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print(f"  Total Size: {get_size(partition_usage.total)}")
            print(f"  Used: {get_size(partition_usage.used)}")
            print(f"  Free: {get_size(partition_usage.free)}")
            print(f"  Percentage: {partition_usage.percent}%")
        except PermissionError:
            continue

    # --- ИСПРАВЛЕННЫЙ БЛОК СЕТИ (отступы выровнены) ---
    print("="*40, "Network Information", "="*40)
    hostname = socket.gethostname()
    print(f"Hostname: {hostname}")
    
    # Безопасный способ получить IP без DNS
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        IPAddr = s.getsockname()[0]
    except Exception:
        IPAddr = '127.0.0.1'
    finally:
        s.close()
        
    print(f"IP Address: {IPAddr}")
    
    # MAC-адрес
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    print(f"MAC Address: {mac}")

if __name__ == "__main__":
    # Если нет psutil, скажет как установить
    try:
        collect_info()
    except ImportError:
        print("Для работы нужен модуль psutil. Установи его командой: pip install psutil")
