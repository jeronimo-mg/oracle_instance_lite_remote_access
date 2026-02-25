import shutil
import subprocess
import time
import os
import glob

def test_weston_installed():
    """Verify weston is in PATH."""
    assert shutil.which('weston') is not None, "weston is not installed or not in PATH"

def test_weston_vnc_backend_available():
    """Verify vnc-backend.so is available."""
    # Search for vnc-backend.so in common lib paths
    vnc_backend = glob.glob('/usr/lib64/libweston-*/vnc-backend.so')
    assert len(vnc_backend) > 0, "Weston VNC backend is not available"

def test_weston_vnc_runs_with_script():
    """Verify weston can be started with the start-weston.sh script."""
    try:
        # Start weston using our script
        proc = subprocess.Popen(['bash', 'scripts/start-weston.sh'], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        time.sleep(3) # Give it more time to start
        
        # Check if process is still running
        if proc.poll() is None:
            # Process is running
            proc.terminate()
            proc.wait()
            assert True
        else:
            stderr = proc.stderr.read().decode()
            assert False, f"Weston script failed to start: {stderr}"
            
    except Exception as e:
        assert False, f"An error occurred while starting Weston via script: {e}"

if __name__ == "__main__":
    try:
        test_weston_installed()
        print("PASS: test_weston_installed")
    except AssertionError as e:
        print(f"FAIL: {e}")
        
    try:
        test_weston_vnc_backend_available()
        print("PASS: test_weston_vnc_backend_available")
    except AssertionError as e:
        print(f"FAIL: {e}")

    try:
        test_weston_vnc_runs_with_script()
        print("PASS: test_weston_vnc_runs_with_script")
    except AssertionError as e:
        print(f"FAIL: {e}")
