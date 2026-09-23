def test_legend_title_fontsize():
    # test the title_fontsize kwarg
    fig, ax = plt.subplots()
    ax.plot(range(10))
    leg = ax.legend(title='Aardvark', title_fontsize=22)
    assert leg.get_title().get_fontsize() == 22
