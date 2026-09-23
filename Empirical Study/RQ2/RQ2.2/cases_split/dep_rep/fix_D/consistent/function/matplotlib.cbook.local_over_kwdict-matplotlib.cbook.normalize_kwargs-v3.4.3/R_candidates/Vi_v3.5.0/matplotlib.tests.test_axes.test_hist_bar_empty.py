@image_comparison(['hist_bar_empty.png'], remove_text=True)
def test_hist_bar_empty():
    # From #3886: creating hist from empty dataset raises ValueError
    ax = plt.gca()
    ax.hist([], histtype='bar')
