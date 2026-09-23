def test_datetime_masked():
    # make sure that all-masked data falls back to the viewlim
    # set in convert.axisinfo....
    x = np.array([datetime.datetime(2017, 1, n) for n in range(1, 6)])
    y = np.array([1, 2, 3, 4, 5])
    m = np.ma.masked_greater(y, 0)

    fig, ax = plt.subplots()
    ax.plot(x, m)
    dt = mdates.date2num(np.datetime64('0000-12-31'))
    assert ax.get_xlim() == (730120.0 + dt, 733773.0 + dt)
