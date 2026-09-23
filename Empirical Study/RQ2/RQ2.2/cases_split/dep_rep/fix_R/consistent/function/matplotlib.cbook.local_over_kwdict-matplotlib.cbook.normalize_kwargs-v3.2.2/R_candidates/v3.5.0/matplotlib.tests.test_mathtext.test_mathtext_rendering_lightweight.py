@pytest.mark.parametrize('index, text', enumerate(lightweight_math_tests),
                         ids=range(len(lightweight_math_tests)))
@pytest.mark.parametrize('fontset', ['dejavusans'])
@pytest.mark.parametrize('baseline_images', ['mathtext1'], indirect=True)
@image_comparison(baseline_images=None, extensions=['png'])
def test_mathtext_rendering_lightweight(baseline_images, fontset, index, text):
    fig = plt.figure(figsize=(5.25, 0.75))
    fig.text(0.5, 0.5, text, math_fontfamily=fontset,
             horizontalalignment='center', verticalalignment='center')
