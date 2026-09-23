@image_comparison(['fancy'], remove_text=True)
def test_fancy():
    # using subplot triggers some offsetbox functionality untested elsewhere
    plt.subplot(121)
    plt.plot([5] * 10, 'o--', label='XX')
    plt.scatter(np.arange(10), np.arange(10, 0, -1), label='XX\nXX')
    plt.errorbar(np.arange(10), np.arange(10), xerr=0.5,
                 yerr=0.5, label='XX')
    plt.legend(loc="center left", bbox_to_anchor=[1.0, 0.5],
               ncol=2, shadow=True, title="My legend", numpoints=1)
