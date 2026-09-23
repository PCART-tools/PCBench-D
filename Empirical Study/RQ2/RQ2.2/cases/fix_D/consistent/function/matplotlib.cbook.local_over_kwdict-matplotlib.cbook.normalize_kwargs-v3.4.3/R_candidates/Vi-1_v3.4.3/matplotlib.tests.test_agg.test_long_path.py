def test_long_path():
    buff = io.BytesIO()

    fig, ax = plt.subplots()
    np.random.seed(0)
    points = np.random.rand(70000)
    ax.plot(points)
    fig.savefig(buff, format='png')
