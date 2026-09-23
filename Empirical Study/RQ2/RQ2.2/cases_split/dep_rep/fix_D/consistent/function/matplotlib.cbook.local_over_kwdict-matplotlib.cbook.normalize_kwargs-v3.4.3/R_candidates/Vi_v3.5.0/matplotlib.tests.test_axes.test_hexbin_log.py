@image_comparison(['hexbin_log.png'], style='mpl20')
def test_hexbin_log():
    # Issue #1636 (and also test log scaled colorbar)

    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    np.random.seed(19680801)
    n = 100000
    x = np.random.standard_normal(n)
    y = 2.0 + 3.0 * x + 4.0 * np.random.standard_normal(n)
    y = np.power(2, y * 0.5)

    fig, ax = plt.subplots()
    h = ax.hexbin(x, y, yscale='log', bins='log',
                  marginals=True, reduce_C_function=np.sum)
    plt.colorbar(h)
