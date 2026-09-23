@image_comparison(['date_timezone_x_and_y.png'], tol=1.0)
def test_date_timezone_x_and_y():
    # Tests issue 5575
    UTC = datetime.timezone.utc
    time_index = [datetime.datetime(2016, 2, 22, hour=x, tzinfo=UTC)
                  for x in range(3)]

    # Same Timezone
    plt.figure(figsize=(20, 12))
    plt.subplot(2, 1, 1)
    plt.plot_date(time_index, time_index, tz='UTC', ydate=True)

    # Different Timezone
    plt.subplot(2, 1, 2)
    plt.plot_date(time_index, time_index, tz='US/Eastern', ydate=True)
