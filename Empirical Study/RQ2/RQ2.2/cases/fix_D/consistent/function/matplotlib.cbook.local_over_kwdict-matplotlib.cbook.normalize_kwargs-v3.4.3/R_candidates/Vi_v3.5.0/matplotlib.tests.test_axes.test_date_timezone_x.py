@image_comparison(['date_timezone_x.png'], tol=1.0)
def test_date_timezone_x():
    # Tests issue 5575
    time_index = [datetime.datetime(2016, 2, 22, hour=x,
                                    tzinfo=dateutil.tz.gettz('Canada/Eastern'))
                  for x in range(3)]

    # Same Timezone
    plt.figure(figsize=(20, 12))
    plt.subplot(2, 1, 1)
    plt.plot_date(time_index, [3] * 3, tz='Canada/Eastern')

    # Different Timezone
    plt.subplot(2, 1, 2)
    plt.plot_date(time_index, [3] * 3, tz='UTC')
