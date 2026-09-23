@image_comparison(['imshow'], remove_text=True, style='mpl20')
def test_imshow():
    fig, ax = plt.subplots()
    arr = np.arange(100).reshape((10, 10))
    ax.imshow(arr, interpolation="bilinear", extent=(1, 2, 1, 2))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
