@image_comparison(['bbox_inches_tight_raster'],
                  remove_text=True, savefig_kwarg={'bbox_inches': 'tight'})
def test_bbox_inches_tight_raster():
    """Test rasterization with tight_layout"""
    fig, ax = plt.subplots()
    ax.plot([1.0, 2.0], rasterized=True)
