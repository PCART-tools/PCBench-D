@pytest.mark.backend('TkAgg', skip_on_importerror=True)
@pytest.mark.flaky(reruns=3)
def test_figuremanager_cleans_own_mainloop():
    script = '''
import tkinter
import time
import matplotlib.pyplot as plt
import threading
from matplotlib.cbook import _get_running_interactive_framework

root = tkinter.Tk()
plt.plot([1, 2, 3], [1, 2, 5])

def target():
    while not 'tk' == _get_running_interactive_framework():
        time.sleep(.01)
    plt.close()
    if show_finished_event.wait():
        print('success')

show_finished_event = threading.Event()
thread = threading.Thread(target=target, daemon=True)
thread.start()
plt.show(block=True)  # testing if this function hangs
show_finished_event.set()
thread.join()

'''
    try:
        proc = subprocess.run(
            [sys.executable, "-c", script],
            env={**os.environ,
                 "MPLBACKEND": "TkAgg",
                 "SOURCE_DATE_EPOCH": "0"},
            timeout=_test_timeout,
            stdout=subprocess.PIPE,
            universal_newlines=True,
            check=True
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Most likely plot.show(block=True) hung")
    except subprocess.CalledProcessError:
        pytest.fail("Subprocess failed to test intended behavior")
    assert proc.stdout.count("success") == 1
