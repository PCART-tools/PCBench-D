@image_comparison(['streamplot_colormap'],
                  tol=.04, remove_text=True, style='mpl20')
def test_colormap():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    X, Y, U, V = velocity_field()
    plt.streamplot(X, Y, U, V, color=U, density=0.6, linewidth=2,
                   cmap=plt.cm.autumn)
    plt.colorbar()
