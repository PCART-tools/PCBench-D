def test_mathtext_to_png(tmpdir):
    with _api.suppress_matplotlib_deprecation_warning():
        mt = mathtext.MathTextParser('bitmap')
        mt.to_png(str(tmpdir.join('example.png')), '$x^2$')
        mt.to_png(io.BytesIO(), '$x^2$')
