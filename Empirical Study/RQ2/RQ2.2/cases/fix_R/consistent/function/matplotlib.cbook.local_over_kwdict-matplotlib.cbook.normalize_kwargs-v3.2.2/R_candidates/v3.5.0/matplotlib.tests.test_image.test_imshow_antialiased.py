@pytest.mark.parametrize(
    "img_size, fig_size, interpolation",
    [(5, 2, "hanning"),  # data larger than figure.
     (5, 5, "nearest"),  # exact resample.
     (5, 10, "nearest"),  # double sample.
     (3, 2.9, "hanning"),  # <3 upsample.
     (3, 9.1, "nearest"),  # >3 upsample.
     ])
@check_figures_equal(extensions=['png'])
def test_imshow_antialiased(fig_test, fig_ref,
                            img_size, fig_size, interpolation):
    np.random.seed(19680801)
    dpi = plt.rcParams["savefig.dpi"]
    A = np.random.rand(int(dpi * img_size), int(dpi * img_size))
    for fig in [fig_test, fig_ref]:
        fig.set_size_inches(fig_size, fig_size)
    ax = fig_test.subplots()
    ax.set_position([0, 0, 1, 1])
    ax.imshow(A, interpolation='antialiased')
    ax = fig_ref.subplots()
    ax.set_position([0, 0, 1, 1])
    ax.imshow(A, interpolation=interpolation)
