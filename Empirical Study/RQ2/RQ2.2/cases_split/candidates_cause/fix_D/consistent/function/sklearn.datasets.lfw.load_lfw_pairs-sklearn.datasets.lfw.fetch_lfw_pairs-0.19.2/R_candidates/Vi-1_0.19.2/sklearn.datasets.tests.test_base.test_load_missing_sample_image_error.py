def test_load_missing_sample_image_error():
    have_PIL = True
    try:
        try:
            from scipy.misc import imread
        except ImportError:
            from scipy.misc.pilutil import imread  # noqa
    except ImportError:
        have_PIL = False
    if have_PIL:
        assert_raises(AttributeError, load_sample_image,
                      'blop.jpg')
    else:
        warnings.warn("Could not load sample images, PIL is not available.")
