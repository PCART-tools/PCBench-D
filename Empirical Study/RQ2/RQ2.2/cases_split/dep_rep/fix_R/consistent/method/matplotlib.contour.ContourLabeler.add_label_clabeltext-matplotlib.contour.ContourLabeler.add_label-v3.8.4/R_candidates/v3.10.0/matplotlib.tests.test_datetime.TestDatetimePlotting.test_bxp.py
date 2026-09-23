    @mpl.style.context("default")
    def test_bxp(self):
        mpl.rcParams["date.converter"] = 'concise'
        fig, ax = plt.subplots()
        data = [{
            "med": datetime.datetime(2020, 1, 15),
            "q1": datetime.datetime(2020, 1, 10),
            "q3": datetime.datetime(2020, 1, 20),
            "whislo": datetime.datetime(2020, 1, 5),
            "whishi": datetime.datetime(2020, 1, 25),
            "fliers": [
                datetime.datetime(2020, 1, 3),
                datetime.datetime(2020, 1, 27)
            ]
        }]
        ax.bxp(data, orientation='horizontal')
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter("%Y-%m-%d"))
        ax.set_title('Box plot with datetime data')
