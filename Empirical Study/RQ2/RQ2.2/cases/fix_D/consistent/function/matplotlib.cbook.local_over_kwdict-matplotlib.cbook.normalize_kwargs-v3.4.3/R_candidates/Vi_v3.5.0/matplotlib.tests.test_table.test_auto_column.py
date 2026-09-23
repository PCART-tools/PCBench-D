@image_comparison(['table_auto_column.png'])
def test_auto_column():
    fig = plt.figure()

    # iterable list input
    ax1 = fig.add_subplot(4, 1, 1)
    ax1.axis('off')
    tb1 = ax1.table(
        cellText=[['Fit Text', 2],
                  ['very long long text, Longer text than default', 1]],
        rowLabels=["A", "B"],
        colLabels=["Col1", "Col2"],
        loc="center")
    tb1.auto_set_font_size(False)
    tb1.set_fontsize(12)
    tb1.auto_set_column_width([-1, 0, 1])

    # iterable tuple input
    ax2 = fig.add_subplot(4, 1, 2)
    ax2.axis('off')
    tb2 = ax2.table(
        cellText=[['Fit Text', 2],
                  ['very long long text, Longer text than default', 1]],
        rowLabels=["A", "B"],
        colLabels=["Col1", "Col2"],
        loc="center")
    tb2.auto_set_font_size(False)
    tb2.set_fontsize(12)
    tb2.auto_set_column_width((-1, 0, 1))

    # 3 single inputs
    ax3 = fig.add_subplot(4, 1, 3)
    ax3.axis('off')
    tb3 = ax3.table(
        cellText=[['Fit Text', 2],
                  ['very long long text, Longer text than default', 1]],
        rowLabels=["A", "B"],
        colLabels=["Col1", "Col2"],
        loc="center")
    tb3.auto_set_font_size(False)
    tb3.set_fontsize(12)
    tb3.auto_set_column_width(-1)
    tb3.auto_set_column_width(0)
    tb3.auto_set_column_width(1)

    # 4 non integer iterable input
    ax4 = fig.add_subplot(4, 1, 4)
    ax4.axis('off')
    tb4 = ax4.table(
        cellText=[['Fit Text', 2],
                  ['very long long text, Longer text than default', 1]],
        rowLabels=["A", "B"],
        colLabels=["Col1", "Col2"],
        loc="center")
    tb4.auto_set_font_size(False)
    tb4.set_fontsize(12)
    tb4.auto_set_column_width("-101")
