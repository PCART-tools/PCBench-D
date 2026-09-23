@pytest.mark.parametrize("use_line_collection", [True, False],
                         ids=['w/ line collection', 'w/o line collection'])
@image_comparison(['stem.png'], style='mpl20', remove_text=True)
def test_stem(use_line_collection):
    x = np.linspace(0.1, 2 * np.pi, 100)

    fig, ax = plt.subplots()
    # Label is a single space to force a legend to be drawn, but to avoid any
    # text being drawn
    ax.stem(x, np.cos(x),
            linefmt='C2-.', markerfmt='k+', basefmt='C1-.', label=' ',
            use_line_collection=use_line_collection)
    ax.legend()
