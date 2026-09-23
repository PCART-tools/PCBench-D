@check_figures_equal(extensions=['png'])
def test_imshow_zoom(fig_test, fig_ref):
    # should be less than 3 upsample, so should be nearest...
    np.random.seed(19680801)
    dpi = plt.rcParams["savefig.dpi"]
    A = np.random.rand(int(dpi * 3), int(dpi * 3))
    for fig in [fig_test, fig_ref]:
        fig.set_size_inches(2.9, 2.9)
    axs = fig_test.subplots()
    axs.imshow(A, interpolation='antialiased')
    axs.set_xlim([10, 20])
    axs.set_ylim([10, 20])
    axs = fig_ref.subplots()
    axs.imshow(A, interpolation='nearest')
    axs.set_xlim([10, 20])
    axs.set_ylim([10, 20])
