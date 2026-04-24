import platform
import ctypes
import sys
from datetime import datetime, time
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List

# ==========================================
# Interfaces (Open/Closed & Dependency Inversion)
# ==========================================

class WebsiteProvider(ABC):
    @abstractmethod
    def get_websites(self) -> List[str]:
        pass

class ScheduleManager(ABC):
    @abstractmethod
    def is_blocking_time(self) -> bool:
        pass

# ==========================================
# Implementations
# ==========================================

class FileWebsiteProvider(WebsiteProvider):
    """Reads and sanitizes the list of websites from a text file."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def get_websites(self) -> List[str]:
        if not self.file_path.exists():
            print(f"Error: {self.file_path} not found.")
            return []
        
        with open(self.file_path, "r") as file:
            # Strip whitespace and ignore empty lines
            return [line.strip() for line in file if line.strip()]

class DailyScheduleManager(ScheduleManager):
    """Checks if the current time falls within daily working hours."""
    
    def __init__(self, start_time: time, end_time: time):
        self.start_time = start_time
        self.end_time = end_time

    def is_blocking_time(self) -> bool:
        current_time = datetime.now().time()
        return self.start_time <= current_time <= self.end_time

class HostsFileModifier:
    """Handles the low-level reading and writing of the OS hosts file."""
    
    REDIRECT_IP = "127.0.0.1"

    def __init__(self):
        self.hosts_path = self._get_hosts_path()

    def _get_hosts_path(self) -> Path:
        if platform.system() == "Windows":
            return Path(r"C:\Windows\System32\drivers\etc\hosts")
        # You can add Mac/Linux support here later without breaking existing code
        raise OSError("Unsupported Operating System. This script requires Windows.")

    def block(self, websites: List[str]):
        """Appends websites to the hosts file if they aren't already there."""
        try:
            with open(self.hosts_path, "r+") as file:
                content = file.read()
                for website in websites:
                    if website not in content:
                        file.write(f"{self.REDIRECT_IP} {website}\n")
            print("Action: Websites successfully BLOCKED.")
        except PermissionError:
            print("Permission Denied: Please run this script as an Administrator.")
            sys.exit(1)

    def unblock(self, websites: List[str]):
        """Removes specific websites from the hosts file."""
        try:
            with open(self.hosts_path, "r") as file:
                lines = file.readlines()

            with open(self.hosts_path, "w") as file:
                for line in lines:
                    # If the line does NOT contain any of our blocked websites, keep it
                    if not any(website in line for website in websites):
                        file.write(line)
            print("Action: Websites successfully UNBLOCKED.")
        except PermissionError:
            print("Permission Denied: Please run this script as an Administrator.")
            sys.exit(1)

# ==========================================
# Orchestrator
# ==========================================

class WebsiteBlocker:
    """Coordinates the checking of schedules and modification of files."""
    
    def __init__(self, provider: WebsiteProvider, schedule: ScheduleManager, modifier: HostsFileModifier):
        self.provider = provider
        self.schedule = schedule
        self.modifier = modifier

    def run_once(self):
        """Executes a single check and updates the hosts file accordingly."""
        websites = self.provider.get_websites()
        if not websites:
            print("No websites to block. Exiting.")
            return

        if self.schedule.is_blocking_time():
            print("Status: Working hours active.")
            self.modifier.block(websites)
        else:
            print("Status: Free time active.")
            self.modifier.unblock(websites)

# ==========================================
# Main Execution
# ==========================================

def is_admin() -> bool:
    """Checks if the script is running with Windows Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

if __name__ == "__main__":
    if not is_admin():
        print("CRITICAL ERROR: Modifying the hosts file requires Administrator privileges.")
        print("Please right-click your command prompt/IDE and select 'Run as Administrator'.")
        sys.exit(1)

    # Dependency Injection: Wiring the application together
    # Set your working hours here (e.g., 9:00 AM to 5:00 PM)
    work_start = time(9, 0, 0)
    work_end = time(17, 0, 0)

    website_provider = FileWebsiteProvider("website_lists.txt")
    schedule_manager = DailyScheduleManager(work_start, work_end)
    host_modifier = HostsFileModifier()

    blocker = WebsiteBlocker(website_provider, schedule_manager, host_modifier)
    
    print(f"Running blocker check at {datetime.now().strftime('%H:%M:%S')}...")
    blocker.run_once()
