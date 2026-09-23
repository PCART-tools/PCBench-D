@pytest.mark.parametrize(
    'index, text', enumerate(font_tests), ids=range(len(font_tests)))
@pytest.mark.parametrize(
    'fontset', ['cm', 'stix', 'stixsans', 'dejavusans', 'dejavuserif'])
@pytest.mark.parametrize('baseline_images', ['mathfont'], indirect=True)
@image_comparison(baseline_images=None, extensions=['png'])
def test_mathfont_rendering(baseline_images, fontset, index, text):
    mpl.rcParams['mathtext.fontset'] = fontset
    fig = plt.figure(figsize=(5.25, 0.75))
    fig.text(0.5, 0.5, text,
             horizontalalignment='center', verticalalignment='center')
