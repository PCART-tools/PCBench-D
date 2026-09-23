@image_comparison(['contour_hatching'], remove_text=True, style='mpl20')
def test_contour_hatching():
    x, y, z = contour_dat()
    fig, ax = plt.subplots()
    ax.contourf(x, y, z, 7, hatches=['/', '\\', '//', '-'],
                cmap=plt.get_cmap('gray'),
                extend='both', alpha=0.5)
