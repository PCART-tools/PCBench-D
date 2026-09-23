def test_ginput(recwarn):  # recwarn undoes warn filters at exit.
    warnings.filterwarnings("ignore", "cannot show the figure")
    fig, ax = plt.subplots()

    def single_press():
        fig.canvas.button_press_event(*ax.transData.transform((.1, .2)), 1)

    Timer(.1, single_press).start()
    assert fig.ginput() == [(.1, .2)]

    def multi_presses():
        fig.canvas.button_press_event(*ax.transData.transform((.1, .2)), 1)
        fig.canvas.key_press_event("backspace")
        fig.canvas.button_press_event(*ax.transData.transform((.3, .4)), 1)
        fig.canvas.button_press_event(*ax.transData.transform((.5, .6)), 1)
        fig.canvas.button_press_event(*ax.transData.transform((0, 0)), 2)

    Timer(.1, multi_presses).start()
    np.testing.assert_allclose(fig.ginput(3), [(.3, .4), (.5, .6)])
