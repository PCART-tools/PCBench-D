def test_suptitle():
    fig, ax = plt.subplots(tight_layout=True)
    st = fig.suptitle("foo")
    t = ax.set_title("bar")
    fig.canvas.draw()
    assert st.get_window_extent().y0 > t.get_window_extent().y1
