def test_subfigure_tightbbox():
    # test that we can get the tightbbox with a subfigure...
    fig = plt.figure(constrained_layout=True)
    sub = fig.subfigures(1, 2)

    np.testing.assert_allclose(
            fig.get_tightbbox(fig.canvas.get_renderer()).width, 0.1)
