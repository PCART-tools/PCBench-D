@pytest.mark.backend('TkAgg', skip_on_importerror=True)
def test_figuremanager_preserves_host_mainloop():
    script = """
import tkinter
import matplotlib.pyplot as plt
success = False

def do_plot():
    plt.figure()
    plt.plot([1, 2], [3, 5])
    plt.close()
    root.after(0, legitimate_quit)

def legitimate_quit():
    root.quit()
    global success
    success = True

root = tkinter.Tk()
root.after(0, do_plot)
root.mainloop()

if success:
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
            check=True,
            universal_newlines=True,
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Subprocess timed out")
    except subprocess.CalledProcessError:
        pytest.fail("Subprocess failed to test intended behavior")
    else:
        assert proc.stdout.count("success") == 1
