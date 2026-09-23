@image_comparison(['image_interps'], style='mpl20')
def test_image_interps():
    """Make the basic nearest, bilinear and bicubic interps."""
    # Remove this line when this test image is regenerated.
    plt.rcParams['text.kerning_factor'] = 6

    X = np.arange(100).reshape(5, 20)

    fig, (ax1, ax2, ax3) = plt.subplots(3)
    ax1.imshow(X, interpolation='nearest')
    ax1.set_title('three interpolations')
    ax1.set_ylabel('nearest')

    ax2.imshow(X, interpolation='bilinear')
    ax2.set_ylabel('bilinear')

    ax3.imshow(X, interpolation='bicubic')
    ax3.set_ylabel('bicubic')
