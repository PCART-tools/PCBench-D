@image_comparison(['hatching'], remove_text=True, style='default')
def test_hatching():
    fig, ax = plt.subplots(1, 1)

    # Default hatch color.
    rect1 = mpatches.Rectangle((0, 0), 3, 4, hatch='/')
    ax.add_patch(rect1)

    rect2 = mcollections.RegularPolyCollection(4, sizes=[16000],
                                               offsets=[(1.5, 6.5)],
                                               transOffset=ax.transData,
                                               hatch='/')
    ax.add_collection(rect2)

    # Ensure edge color is not applied to hatching.
    rect3 = mpatches.Rectangle((4, 0), 3, 4, hatch='/', edgecolor='C1')
    ax.add_patch(rect3)

    rect4 = mcollections.RegularPolyCollection(4, sizes=[16000],
                                               offsets=[(5.5, 6.5)],
                                               transOffset=ax.transData,
                                               hatch='/', edgecolor='C1')
    ax.add_collection(rect4)

    ax.set_xlim(0, 7)
    ax.set_ylim(0, 9)
