import subprocess

class ServiceManager:
    def __init__(self, services=None):
        self.services = services or []

    def check_status(self, service_name):
        """Returns True if the service is active."""
        try:
            result = subprocess.run(['systemctl', 'is-active', service_name], capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

    def restart_service(self, service_name):
        """Restarts the service using sudo."""
        try:
            result = subprocess.run(['sudo', 'systemctl', 'restart', service_name], capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

    def get_all_statuses(self):
        """Returns a dictionary with service names and their statuses."""
        results = {}
        for service in self.services:
            is_active = self.check_status(service)
            results[service] = 'active' if is_active else 'inactive'
        return results

if __name__ == "__main__":
    # Quick manual check if run directly
    mgr = ServiceManager(services=['weston.service', 'novnc.service', 'tailscaled.service'])
    print(mgr.get_all_statuses())
