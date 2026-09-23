@pytest.mark.parametrize("use_line_collection", [True, False],
                         ids=['w/ line collection', 'w/o line collection'])
@image_comparison(['stem_orientation.png'], style='mpl20', remove_text=True)
def test_stem_orientation(use_line_collection):
    x = np.linspace(0.1, 2*np.pi, 50)

    fig, ax = plt.subplots()
    ax.stem(x, np.cos(x),
            linefmt='C2-.', markerfmt='kx', basefmt='C1-.',
            use_line_collection=use_line_collection, orientation='horizontal')
