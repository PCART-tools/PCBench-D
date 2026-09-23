def test_waitforbuttonpress(recwarn):  # recwarn undoes warn filters at exit.
    warnings.filterwarnings("ignore", "cannot show the figure")
    fig = plt.figure()
    assert fig.waitforbuttonpress(timeout=.1) is None
    Timer(.1, fig.canvas.key_press_event, ("z",)).start()
    assert fig.waitforbuttonpress() is True
    Timer(.1, fig.canvas.button_press_event, (0, 0, 1)).start()
    assert fig.waitforbuttonpress() is False
