@pytest.mark.parametrize(
    'index, text', enumerate(math_tests), ids=range(len(math_tests)))
@pytest.mark.parametrize(
    'fontset', ['cm', 'stix', 'stixsans', 'dejavusans', 'dejavuserif'])
@pytest.mark.parametrize('baseline_images', ['mathtext'], indirect=True)
@image_comparison(baseline_images=None)
def test_mathtext_rendering(baseline_images, fontset, index, text):
    mpl.rcParams['mathtext.fontset'] = fontset
    fig = plt.figure(figsize=(5.25, 0.75))
    fig.text(0.5, 0.5, text,
             horizontalalignment='center', verticalalignment='center')
