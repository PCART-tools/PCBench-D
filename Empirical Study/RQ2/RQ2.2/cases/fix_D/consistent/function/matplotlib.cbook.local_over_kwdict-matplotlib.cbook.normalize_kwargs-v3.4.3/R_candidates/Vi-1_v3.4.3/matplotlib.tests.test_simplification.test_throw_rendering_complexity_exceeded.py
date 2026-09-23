def test_throw_rendering_complexity_exceeded():
    plt.rcParams['path.simplify'] = False
    xx = np.arange(200000)
    yy = np.random.rand(200000)
    yy[1000] = np.nan

    fig, ax = plt.subplots()
    ax.plot(xx, yy)
    with pytest.raises(OverflowError):
        fig.savefig(io.BytesIO())
