@pytest.mark.parametrize("fmt,counted",
                         [("ps", b" colorimage"), ("svg", b"<image")])
@pytest.mark.parametrize("composite_image,count", [(True, 1), (False, 2)])
def test_composite(fmt, counted, composite_image, count):
    # Test that figures can be saved with and without combining multiple images
    # (on a single set of axes) into a single composite image.
    X, Y = np.meshgrid(np.arange(-5, 5, 1), np.arange(-5, 5, 1))
    Z = np.sin(Y ** 2)

    fig, ax = plt.subplots()
    ax.set_xlim(0, 3)
    ax.imshow(Z, extent=[0, 1, 0, 1])
    ax.imshow(Z[::-1], extent=[2, 3, 0, 1])
    plt.rcParams['image.composite_image'] = composite_image
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt)
    assert buf.getvalue().count(counted) == count
