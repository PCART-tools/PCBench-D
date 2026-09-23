@pytest.mark.skipif(sys.platform != "linux", reason="this a linux-only test")
@pytest.mark.backend('QtAgg', skip_on_importerror=True)
def test_lazy_linux_headless():
    test_script = """
import os
import sys

# make it look headless
os.environ.pop('DISPLAY', None)
os.environ.pop('WAYLAND_DISPLAY', None)

# we should fast-track to Agg
import matplotlib.pyplot as plt
plt.get_backend() == 'agg'
assert 'PyQt5' not in sys.modules

# make sure we really have pyqt installed
import PyQt5
assert 'PyQt5' in sys.modules

# try to switch and make sure we fail with ImportError
try:
    plt.switch_backend('qt5agg')
except ImportError:
    ...
else:
    sys.exit(1)

"""
    proc = subprocess.run([sys.executable, "-c", test_script],
                          env={**os.environ, "MPLBACKEND": ""})
    if proc.returncode:
        pytest.fail("The subprocess returned with non-zero exit status "
                    f"{proc.returncode}.")
