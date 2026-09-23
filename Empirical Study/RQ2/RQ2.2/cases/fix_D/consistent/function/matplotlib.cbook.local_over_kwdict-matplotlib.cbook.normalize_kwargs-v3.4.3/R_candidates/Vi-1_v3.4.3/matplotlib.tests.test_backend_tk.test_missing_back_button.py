@pytest.mark.backend('TkAgg', skip_on_importerror=True)
def test_missing_back_button():
    script = """
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
class Toolbar(NavigationToolbar2Tk):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2Tk.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom')]

fig = plt.figure()
print("setup complete")
# this should not raise
Toolbar(fig.canvas, fig.canvas.manager.window)
print("success")
"""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", script],
            env={**os.environ,
                 "MPLBACKEND": "TkAgg",
                 "SOURCE_DATE_EPOCH": "0"},
            timeout=_test_timeout,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Subprocess timed out")
    else:
        assert proc.stdout.count("setup complete") == 1
        assert proc.stdout.count("success") == 1
        # Checking return code late so the stdout assertions happen first
        if proc.returncode:
            pytest.fail("Subprocess failed to test intended behavior")
