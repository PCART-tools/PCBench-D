@image_comparison(['hexbin_empty.png'], remove_text=True)
def test_hexbin_empty():
    # From #3886: creating hexbin from empty dataset raises ValueError
    ax = plt.gca()
    ax.hexbin([], [])
