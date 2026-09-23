def test_pick():
    fig = plt.figure()
    fig.text(.5, .5, "hello", ha="center", va="center", picker=True)
    fig.canvas.draw()
    picks = []
    fig.canvas.mpl_connect("pick_event", lambda event: picks.append(event))
    start_event = MouseEvent(
        "button_press_event", fig.canvas, *fig.transFigure.transform((.5, .5)),
        MouseButton.LEFT)
    fig.canvas.callbacks.process(start_event.name, start_event)
    assert len(picks) == 1
