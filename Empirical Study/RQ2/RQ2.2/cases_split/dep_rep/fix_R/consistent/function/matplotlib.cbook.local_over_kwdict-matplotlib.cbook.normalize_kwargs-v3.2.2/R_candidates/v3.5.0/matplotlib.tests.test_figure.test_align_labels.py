@image_comparison(['figure_align_labels'], extensions=['png', 'svg'],
                  tol=0 if platform.machine() == 'x86_64' else 0.01)
def test_align_labels():
    fig = plt.figure(tight_layout=True)
    gs = gridspec.GridSpec(3, 3)

    ax = fig.add_subplot(gs[0, :2])
    ax.plot(np.arange(0, 1e6, 1000))
    ax.set_ylabel('Ylabel0 0')
    ax = fig.add_subplot(gs[0, -1])
    ax.plot(np.arange(0, 1e4, 100))

    for i in range(3):
        ax = fig.add_subplot(gs[1, i])
        ax.set_ylabel('YLabel1 %d' % i)
        ax.set_xlabel('XLabel1 %d' % i)
        if i in [0, 2]:
            ax.xaxis.set_label_position("top")
            ax.xaxis.tick_top()
        if i == 0:
            for tick in ax.get_xticklabels():
                tick.set_rotation(90)
        if i == 2:
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()

    for i in range(3):
        ax = fig.add_subplot(gs[2, i])
        ax.set_xlabel(f'XLabel2 {i}')
        ax.set_ylabel(f'YLabel2 {i}')

        if i == 2:
            ax.plot(np.arange(0, 1e4, 10))
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
            for tick in ax.get_xticklabels():
                tick.set_rotation(90)

    fig.align_labels()
