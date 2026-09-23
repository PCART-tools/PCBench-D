@image_comparison(['marker_paths.pdf'], remove_text=True)
def test_marker_paths_pdf():
    N = 7

    plt.errorbar(np.arange(N),
                 np.ones(N) + 4,
                 np.ones(N))
    plt.xlim(-1, N)
    plt.ylim(-1, 7)
