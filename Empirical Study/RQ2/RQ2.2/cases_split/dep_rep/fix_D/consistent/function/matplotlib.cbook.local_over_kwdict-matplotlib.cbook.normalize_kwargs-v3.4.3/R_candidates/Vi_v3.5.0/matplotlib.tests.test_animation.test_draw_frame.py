@pytest.mark.parametrize('return_value', [
    # User forgot to return (returns None).
    None,
    # User returned a string.
    'string',
    # User returned an int.
    1,
    # User returns a sequence of other objects, e.g., string instead of Artist.
    ('string', ),
    # User forgot to return a sequence (handled in `animate` below.)
    'artist',
])
def test_draw_frame(return_value):
    # test _draw_frame method

    fig, ax = plt.subplots()
    line, = ax.plot([])

    def animate(i):
        # general update func
        line.set_data([0, 1], [0, i])
        if return_value == 'artist':
            # *not* a sequence
            return line
        else:
            return return_value

    with pytest.raises(RuntimeError):
        animation.FuncAnimation(fig, animate, blit=True)
