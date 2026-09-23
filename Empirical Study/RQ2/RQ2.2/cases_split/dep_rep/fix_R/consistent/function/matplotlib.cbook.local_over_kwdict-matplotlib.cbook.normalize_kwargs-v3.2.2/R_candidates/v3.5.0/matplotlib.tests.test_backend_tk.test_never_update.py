@pytest.mark.backend('TkAgg', skip_on_importerror=True)
@pytest.mark.flaky(reruns=3)
@_isolated_tk_test(success_count=0)
def test_never_update():  # pragma: no cover
    import tkinter
    del tkinter.Misc.update
    del tkinter.Misc.update_idletasks

    import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.show(block=False)

    plt.draw()  # Test FigureCanvasTkAgg.
    fig.canvas.toolbar.configure_subplots()  # Test NavigationToolbar2Tk.

    # Check for update() or update_idletasks() in the event queue, functionally
    # equivalent to tkinter.Misc.update.
    # Must pause >= 1 ms to process tcl idle events plus extra time to avoid
    # flaky tests on slow systems.
    plt.pause(0.1)

    plt.close(fig)  # Test FigureCanvasTk filter_destroy callback
