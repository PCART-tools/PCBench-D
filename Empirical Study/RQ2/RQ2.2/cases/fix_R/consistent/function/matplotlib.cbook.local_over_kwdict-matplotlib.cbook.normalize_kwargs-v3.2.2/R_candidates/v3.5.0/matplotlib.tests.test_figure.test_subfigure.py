@image_comparison(['test_subfigure.png'], style='mpl20',
                  savefig_kwarg={'facecolor': 'teal'},
                  remove_text=False)
def test_subfigure():
    np.random.seed(19680801)
    fig = plt.figure(constrained_layout=True)
    sub = fig.subfigures(1, 2)

    axs = sub[0].subplots(2, 2)
    for ax in axs.flat:
        pc = ax.pcolormesh(np.random.randn(30, 30), vmin=-2, vmax=2)
    sub[0].colorbar(pc, ax=axs)
    sub[0].suptitle('Left Side')

    axs = sub[1].subplots(1, 3)
    for ax in axs.flat:
        pc = ax.pcolormesh(np.random.randn(30, 30), vmin=-2, vmax=2)
    sub[1].colorbar(pc, ax=axs, location='bottom')
    sub[1].suptitle('Right Side')

    fig.suptitle('Figure suptitle', fontsize='xx-large')
