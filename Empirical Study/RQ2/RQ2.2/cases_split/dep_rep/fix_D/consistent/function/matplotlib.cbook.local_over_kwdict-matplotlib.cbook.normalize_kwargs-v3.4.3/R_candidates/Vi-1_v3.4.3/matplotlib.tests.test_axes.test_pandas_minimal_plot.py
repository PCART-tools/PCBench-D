def test_pandas_minimal_plot(pd):
    # smoke test that series and index objcets do not warn
    x = pd.Series([1, 2], dtype="float64")
    plt.plot(x, x)
    plt.plot(x.index, x)
    plt.plot(x)
    plt.plot(x.index)
