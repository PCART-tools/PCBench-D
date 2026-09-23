@image_comparison(["type42_without_prep.eps"], style='mpl20')
def test_type42_font_without_prep():
    # Test whether Type 42 fonts without prep table are properly embedded
    mpl.rcParams["ps.fonttype"] = 42
    mpl.rcParams["mathtext.fontset"] = "stix"

    plt.figtext(0.5, 0.5, "Mass $m$")
