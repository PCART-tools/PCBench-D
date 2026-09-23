@image_comparison(["auto_numticks.png"], style='default')
def test_auto_numticks():
    # Make tiny, empty subplots, verify that there are only 3 ticks.
    plt.subplots(4, 4)
