def test_shared():
    fig, axs = plt.subplots(2, sharex=True)
    fig = pickle.loads(pickle.dumps(fig))
    fig.axes[0].set_xlim(10, 20)
    assert fig.axes[1].get_xlim() == (10, 20)
