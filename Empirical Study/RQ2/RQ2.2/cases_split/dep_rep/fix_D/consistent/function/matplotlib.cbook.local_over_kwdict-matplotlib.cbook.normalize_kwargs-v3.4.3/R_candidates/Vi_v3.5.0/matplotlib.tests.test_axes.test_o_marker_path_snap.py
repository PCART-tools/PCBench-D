@image_comparison(['o_marker_path_snap.png'], savefig_kwarg={'dpi': 72})
def test_o_marker_path_snap():
    fig, ax = plt.subplots()
    ax.margins(.1)
    for ms in range(1, 15):
        ax.plot([1, 2, ], np.ones(2) + ms, 'o', ms=ms)

    for ms in np.linspace(1, 10, 25):
        ax.plot([3, 4, ], np.ones(2) + ms, 'o', ms=ms)
