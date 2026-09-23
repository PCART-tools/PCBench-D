@image_comparison(['date_timezone_y.png'])
def test_date_timezone_y():
    # Tests issue 5575
    time_index = [datetime.datetime(2016, 2, 22, hour=x,
                                    tzinfo=dateutil.tz.gettz('Canada/Eastern'))
                  for x in range(3)]

    # Same Timezone
    plt.figure(figsize=(20, 12))
    plt.subplot(2, 1, 1)
    plt.plot_date([3] * 3,
                  time_index, tz='Canada/Eastern', xdate=False, ydate=True)

    # Different Timezone
    plt.subplot(2, 1, 2)
    plt.plot_date([3] * 3, time_index, tz='UTC', xdate=False, ydate=True)
