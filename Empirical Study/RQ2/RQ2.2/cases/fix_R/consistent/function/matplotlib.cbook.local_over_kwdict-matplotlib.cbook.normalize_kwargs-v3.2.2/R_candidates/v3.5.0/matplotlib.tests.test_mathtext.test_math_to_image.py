def test_math_to_image(tmpdir):
    mathtext.math_to_image('$x^2$', str(tmpdir.join('example.png')))
    mathtext.math_to_image('$x^2$', io.BytesIO())
