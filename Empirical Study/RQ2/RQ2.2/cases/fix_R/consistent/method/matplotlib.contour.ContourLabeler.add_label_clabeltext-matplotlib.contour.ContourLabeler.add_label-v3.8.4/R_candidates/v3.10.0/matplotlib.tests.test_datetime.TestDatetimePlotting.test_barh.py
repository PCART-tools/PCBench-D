    @mpl.style.context("default")
    def test_barh(self):
        mpl.rcParams["date.converter"] = 'concise'
        fig, (ax1, ax2) = plt.subplots(2, 1, layout='constrained')
        birth_date = np.array([datetime.datetime(2020, 4, 10),
                               datetime.datetime(2020, 5, 30),
                               datetime.datetime(2020, 10, 12),
                               datetime.datetime(2020, 11, 15)])
        year_start = datetime.datetime(2020, 1, 1)
        year_end = datetime.datetime(2020, 12, 31)
        age = [21, 53, 20, 24]
        ax1.set_xlabel('Age')
        ax1.set_ylabel('Birth Date')
        ax1.barh(birth_date, width=age, height=datetime.timedelta(days=10))
        ax2.set_xlim(left=year_start, right=year_end)
        ax2.set_xlabel('Birth Date')
        ax2.set_ylabel('Order of Birth Dates')
        ax2.barh(np.arange(4), birth_date-year_start, left=year_start)
