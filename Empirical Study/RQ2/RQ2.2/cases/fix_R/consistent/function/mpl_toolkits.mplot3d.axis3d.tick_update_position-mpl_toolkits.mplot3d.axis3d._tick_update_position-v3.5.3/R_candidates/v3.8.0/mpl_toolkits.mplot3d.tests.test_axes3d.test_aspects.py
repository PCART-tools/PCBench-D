@mpl3d_image_comparison(['aspects.png'], remove_text=False, style='mpl20')
def test_aspects():
    aspects = ('auto', 'equal', 'equalxy', 'equalyz', 'equalxz', 'equal')
    _, axs = plt.subplots(2, 3, subplot_kw={'projection': '3d'})

    for ax in axs.flatten()[0:-1]:
        plot_cuboid(ax, scale=[1, 1, 5])
    # plot a cube as well to cover github #25443
    plot_cuboid(axs[1][2], scale=[1, 1, 1])

    for i, ax in enumerate(axs.flatten()):
        ax.set_title(aspects[i])
        ax.set_box_aspect((3, 4, 5))
        ax.set_aspect(aspects[i], adjustable='datalim')
    axs[1][2].set_title('equal (cube)')
