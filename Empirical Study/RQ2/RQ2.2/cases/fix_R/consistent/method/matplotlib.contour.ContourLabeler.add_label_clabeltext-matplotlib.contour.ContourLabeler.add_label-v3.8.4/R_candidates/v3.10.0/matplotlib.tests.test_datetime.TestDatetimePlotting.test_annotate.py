    @mpl.style.context("default")
    def test_annotate(self):
        mpl.rcParams["date.converter"] = 'concise'
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, layout="constrained")

        start_date = datetime.datetime(2023, 10, 1)
        dates = [start_date + datetime.timedelta(days=i) for i in range(31)]
        data = list(range(1, 32))
        test_text = "Test Text"

        ax1.plot(dates, data)
        ax1.annotate(text=test_text, xy=(dates[15], data[15]))
        ax2.plot(data, dates)
        ax2.annotate(text=test_text, xy=(data[5], dates[26]))
        ax3.plot(dates, dates)
        ax3.annotate(text=test_text, xy=(dates[15], dates[3]))
        ax4.plot(dates, dates)
        ax4.annotate(text=test_text, xy=(dates[5], dates[30]),
                        xytext=(dates[1], dates[7]), arrowprops=dict(facecolor='red'))
