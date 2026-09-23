@image_comparison(['constrained_layout10.png'])
def test_constrained_layout10():
    """Test for handling legend outside axis"""
    fig, axs = plt.subplots(2, 2, constrained_layout=True)
    for ax in axs.flat:
        ax.plot(np.arange(12), label='This is a label')
    ax.legend(loc='center left', bbox_to_anchor=(0.8, 0.5))
