@image_comparison(['fill_between_interpolate_nan'], remove_text=True)
def test_fill_between_interpolate_nan():
    # Tests fix for issue #18986.
    x = np.arange(10)
    y1 = np.asarray([8, 18, np.nan, 18, 8, 18, 24, 18, 8, 18])
    y2 = np.asarray([18, 11, 8, 11, 18, 26, 32, 30, np.nan, np.nan])

    # NumPy <1.19 issues warning 'invalid value encountered in greater_equal'
    # for comparisons that include nan.
    with np.errstate(invalid='ignore'):
        greater2 = y2 >= y1
        greater1 = y1 >= y2

    fig, ax = plt.subplots()

    ax.plot(x, y1, c='k')
    ax.plot(x, y2, c='b')
    ax.fill_between(x, y1, y2, where=greater2, facecolor="green",
                    interpolate=True, alpha=0.5)
    ax.fill_between(x, y1, y2, where=greater1, facecolor="red",
                    interpolate=True, alpha=0.5)
