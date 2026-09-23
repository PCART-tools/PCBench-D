@image_comparison(['imshow_clip'], style='mpl20')
def test_imshow_clip():
    # As originally reported by Gellule Xg <gellule.xg@free.fr>
    # use former defaults to match existing baseline image
    matplotlib.rcParams['image.interpolation'] = 'nearest'

    # Create a NxN image
    N = 100
    (x, y) = np.indices((N, N))
    x -= N//2
    y -= N//2
    r = np.sqrt(x**2+y**2-x*y)

    # Create a contour plot at N/4 and extract both the clip path and transform
    fig, ax = plt.subplots()

    c = ax.contour(r, [N/4])
    x = c.collections[0]
    clip_path = x.get_paths()[0]
    clip_transform = x.get_transform()

    clip_path = mtransforms.TransformedPath(clip_path, clip_transform)

    # Plot the image clipped by the contour
    ax.imshow(r, clip_path=clip_path)
