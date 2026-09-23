    @mpl.style.context("default")
    def test_bar_label(self):
        # Generate some example data with dateTime inputs
        date_list = [datetime.datetime(2023, 1, 1) +
                     datetime.timedelta(days=i) for i in range(5)]
        values = [10, 20, 15, 25, 30]

        # Creating the plot
        fig, ax = plt.subplots(1, 1, figsize=(10, 8), layout='constrained')
        bars = ax.bar(date_list, values)

        # Add labels to the bars using bar_label
        ax.bar_label(bars, labels=[f'{val}%' for val in values],
                     label_type='edge', color='black')
