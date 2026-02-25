import shutil
import subprocess
import time
import os
import glob
import urllib.request

def test_weston_installed():
    """Verify weston is in PATH."""
    assert shutil.which('weston') is not None, "weston is not installed or not in PATH"

def test_novnc_installed():
    """Verify novnc_proxy is in PATH."""
    assert shutil.which('novnc_proxy') is not None, "novnc_proxy is not installed or not in PATH"

def test_weston_service_exists():
    """Verify weston.service exists."""
    assert os.path.exists('/etc/systemd/system/weston.service'), "weston.service does not exist"

def test_novnc_service_exists():
    """Verify novnc.service exists."""
    assert os.path.exists('/etc/systemd/system/novnc.service'), "novnc.service does not exist"

def test_services_available():
    """Verify services are available in systemctl."""
    try:
        # Check if units are listed by systemctl
        out = subprocess.check_output(['systemctl', 'list-unit-files', 'weston.service', 'novnc.service'],
                                      stderr=subprocess.STDOUT).decode()
        assert 'weston.service' in out, "weston.service not in list-unit-files"
        assert 'novnc.service' in out, "novnc.service not in list-unit-files"
        assert True
    except subprocess.CalledProcessError as e:
        assert False, f"Error listing systemctl units: {e.output.decode()}"

if __name__ == "__main__":
    tests = [
        ("test_weston_installed", test_weston_installed),
        ("test_novnc_installed", test_novnc_installed),
        ("test_weston_service_exists", test_weston_service_exists),
        ("test_novnc_service_exists", test_novnc_service_exists),
        ("test_services_available", test_services_available),
    ]
    
    for name, func in tests:
        try:
            func()
            print(f"PASS: {name}")
        except AssertionError as e:
            print(f"FAIL: {name} - {e}")
        except Exception as e:
            print(f"ERR: {name} - {e}")
