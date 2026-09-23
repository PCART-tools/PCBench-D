@image_comparison(['hatching'], remove_text=True, style='default')
def test_hatching():
    # Remove this line when this test image is regenerated.
    plt.rcParams['text.kerning_factor'] = 6

    fig, ax = plt.subplots()

    # Patches
    patch = plt.Rectangle((0, 0), 0.3, 0.3, hatch='xx',
                          label='Patch\ndefault color\nfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0.33, 0), 0.3, 0.3, hatch='||', edgecolor='C1',
                          label='Patch\nexplicit color\nfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0, 0.4), 0.3, 0.3, hatch='xx', fill=False,
                          label='Patch\ndefault color\nunfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0.33, 0.4), 0.3, 0.3, hatch='||', fill=False,
                          edgecolor='C1',
                          label='Patch\nexplicit color\nunfilled')
    ax.add_patch(patch)

    # Paths
    ax.fill_between([0, .15, .3], [.8, .8, .8], [.9, 1.0, .9],
                    hatch='+', label='Path\ndefault color')
    ax.fill_between([.33, .48, .63], [.8, .8, .8], [.9, 1.0, .9],
                    hatch='+', edgecolor='C2', label='Path\nexplicit color')

    ax.set_xlim(-0.01, 1.1)
    ax.set_ylim(-0.01, 1.1)
    ax.legend(handlelength=4, handleheight=4)
