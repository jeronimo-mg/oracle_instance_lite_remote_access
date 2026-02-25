import shutil
import subprocess
import time
import os
import glob
import urllib.request

def test_weston_installed():
    """Verify weston is in PATH."""
    assert shutil.which('weston') is not None, "weston is not installed or not in PATH"

def test_weston_vnc_backend_available():
    """Verify vnc-backend.so is available."""
    vnc_backend = glob.glob('/usr/lib64/libweston-*/vnc-backend.so')
    assert len(vnc_backend) > 0, "Weston VNC backend is not available"

def test_novnc_installed():
    """Verify novnc_proxy is in PATH."""
    assert shutil.which('novnc_proxy') is not None, "novnc_proxy is not installed or not in PATH"

def test_novnc_runs_and_responds():
    """Verify noVNC starts and serves content."""
    try:
        # Start weston first
        weston_proc = subprocess.Popen(['bash', 'scripts/start-weston.sh'], 
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3)
        
        # Start noVNC proxy
        # Listen on 127.0.0.1:6080
        novnc_proc = subprocess.Popen(['novnc_proxy', '--vnc', 'localhost:5900', '--listen', '6080'],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5) # Give it more time
        
        # Check if novnc is responding
        try:
            with urllib.request.urlopen("http://127.0.0.1:6080/vnc.html", timeout=5) as f:
                content = f.read().decode()
                assert "noVNC" in content, "noVNC content not found in response"
                assert True
        except Exception as e:
            # Get some debug info
            if novnc_proc.poll() is not None:
                err = novnc_proc.stderr.read().decode()
                out = novnc_proc.stdout.read().decode()
                assert False, f"noVNC proxy exited prematurely. Out: {out}, Err: {err}"
            else:
                assert False, f"noVNC not responding at http://127.0.0.1:6080/vnc.html: {e}"
        finally:
            novnc_proc.terminate()
            novnc_proc.wait()
            weston_proc.terminate()
            weston_proc.wait()
            
    except Exception as e:
        assert False, f"An error occurred while testing noVNC: {e}"

if __name__ == "__main__":
    tests = [
        ("test_weston_installed", test_weston_installed),
        ("test_weston_vnc_backend_available", test_weston_vnc_backend_available),
        ("test_novnc_installed", test_novnc_installed),
        ("test_novnc_runs_and_responds", test_novnc_runs_and_responds),
    ]
    
    for name, func in tests:
        try:
            func()
            print(f"PASS: {name}")
        except AssertionError as e:
            print(f"FAIL: {name} - {e}")
        except Exception as e:
            print(f"ERR: {name} - {e}")
