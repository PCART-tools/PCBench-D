@pytest.mark.backend('TkAgg', skip_on_importerror=True)
@pytest.mark.flaky(reruns=3)
def test_never_update():
    script = """
import tkinter
del tkinter.Misc.update
del tkinter.Misc.update_idletasks

import matplotlib.pyplot as plt
fig = plt.figure()
plt.show(block=False)

# regression test on FigureCanvasTkAgg
plt.draw()
# regression test on NavigationToolbar2Tk
fig.canvas.toolbar.configure_subplots()

# check for update() or update_idletasks() in the event queue
# functionally equivalent to tkinter.Misc.update
# must pause >= 1 ms to process tcl idle events plus
# extra time to avoid flaky tests on slow systems
plt.pause(0.1)

# regression test on FigureCanvasTk filter_destroy callback
plt.close(fig)
"""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", script],
            env={**os.environ,
                 "MPLBACKEND": "TkAgg",
                 "SOURCE_DATE_EPOCH": "0"},
            timeout=_test_timeout,
            capture_output=True,
            universal_newlines=True,
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Subprocess timed out")
    else:
        # test framework doesn't see tkinter callback exceptions normally
        # see tkinter.Misc.report_callback_exception
        assert "Exception in Tkinter callback" not in proc.stderr
        # make sure we can see other issues
        print(proc.stderr, file=sys.stderr)
        # Checking return code late so the Tkinter assertion happens first
        if proc.returncode:
            pytest.fail("Subprocess failed to test intended behavior")
