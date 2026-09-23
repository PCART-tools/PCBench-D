def test_invisible_axes():
    # invisible axes should not respond to events...
    fig, ax = plt.subplots()
    assert fig.canvas.inaxes((200, 200)) is not None
    ax.set_visible(False)
    assert fig.canvas.inaxes((200, 200)) is None
