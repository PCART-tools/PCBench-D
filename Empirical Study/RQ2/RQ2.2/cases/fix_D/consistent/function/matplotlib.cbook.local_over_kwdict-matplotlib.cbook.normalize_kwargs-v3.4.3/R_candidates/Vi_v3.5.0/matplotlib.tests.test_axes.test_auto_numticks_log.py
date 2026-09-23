@image_comparison(["auto_numticks_log.png"], style='default')
def test_auto_numticks_log():
    # Verify that there are not too many ticks with a large log range.
    fig, ax = plt.subplots()
    matplotlib.rcParams['axes.autolimit_mode'] = 'round_numbers'
    ax.loglog([1e-20, 1e5], [1e-16, 10])
