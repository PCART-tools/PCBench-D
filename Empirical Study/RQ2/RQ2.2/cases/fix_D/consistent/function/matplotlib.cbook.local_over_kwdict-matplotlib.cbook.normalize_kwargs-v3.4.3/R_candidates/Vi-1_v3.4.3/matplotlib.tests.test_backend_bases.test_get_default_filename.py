def test_get_default_filename():
    assert plt.figure().canvas.get_default_filename() == 'image.png'
