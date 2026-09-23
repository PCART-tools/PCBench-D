@image_comparison(['annotation_negative_fig_coords.png'])
def test_annotation_negative_fig_coords():
    fig, ax = plt.subplots()

    ax.annotate('+ pts',
                xytext=[10, 120], textcoords='figure points',
                xy=[10, 120], xycoords='figure points', fontsize=32)
    ax.annotate('- pts',
                xytext=[-10, 180], textcoords='figure points',
                xy=[-10, 180], xycoords='figure points', fontsize=32,
                va='top')
    ax.annotate('+ frac',
                xytext=[0.05, 0.55], textcoords='figure fraction',
                xy=[0.05, 0.55], xycoords='figure fraction', fontsize=32)
    ax.annotate('- frac',
                xytext=[-0.05, 0.5], textcoords='figure fraction',
                xy=[-0.05, 0.5], xycoords='figure fraction', fontsize=32,
                va='top')

    ax.annotate('+ pixels',
                xytext=[50, 50], textcoords='figure pixels',
                xy=[50, 50], xycoords='figure pixels', fontsize=32)
    ax.annotate('- pixels',
                xytext=[-50, 100], textcoords='figure pixels',
                xy=[-50, 100], xycoords='figure pixels', fontsize=32,
                va='top')
