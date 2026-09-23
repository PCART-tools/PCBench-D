@image_comparison(['streamplot_masks_and_nans'],
                  remove_text=True, style='mpl20', tol=0.04 if on_win else 0)
def test_masks_and_nans():
    X, Y, U, V = velocity_field()
    mask = np.zeros(U.shape, dtype=bool)
    mask[40:60, 40:60] = 1
    U[:20, :20] = np.nan
    U = np.ma.array(U, mask=mask)
    # Compatibility for old test image
    ax = plt.figure().subplots()
    ax.set(xlim=(-3.0, 2.9999999999999947),
           ylim=(-3.0000000000000004, 2.9999999999999947))
    with np.errstate(invalid='ignore'):
        ax.streamplot(X, Y, U, V, color=U, cmap=plt.cm.Blues)
