@image_comparison(['bbox_inches_tight'], remove_text=True,
                  savefig_kwarg={'bbox_inches': 'tight'})
def test_bbox_inches_tight():
    #: Test that a figure saved using bbox_inches='tight' is clipped correctly
    data = [[66386, 174296, 75131, 577908, 32015],
            [58230, 381139, 78045, 99308, 160454],
            [89135, 80552, 152558, 497981, 603535],
            [78415, 81858, 150656, 193263, 69638],
            [139361, 331509, 343164, 781380, 52269]]

    col_labels = row_labels = [''] * 5

    rows = len(data)
    ind = np.arange(len(col_labels)) + 0.3  # the x locations for the groups
    cell_text = []
    width = 0.4     # the width of the bars
    yoff = np.zeros(len(col_labels))
    # the bottom values for stacked bar chart
    fig, ax = plt.subplots(1, 1)
    for row in range(rows):
        ax.bar(ind, data[row], width, bottom=yoff, align='edge', color='b')
        yoff = yoff + data[row]
        cell_text.append([''])
    plt.xticks([])
    plt.xlim(0, 5)
    plt.legend([''] * 5, loc=(1.2, 0.2))
    fig.legend([''] * 5, bbox_to_anchor=(0, 0.2), loc='lower left')
    # Add a table at the bottom of the axes
    cell_text.reverse()
    plt.table(cellText=cell_text, rowLabels=row_labels, colLabels=col_labels,
              loc='bottom')
