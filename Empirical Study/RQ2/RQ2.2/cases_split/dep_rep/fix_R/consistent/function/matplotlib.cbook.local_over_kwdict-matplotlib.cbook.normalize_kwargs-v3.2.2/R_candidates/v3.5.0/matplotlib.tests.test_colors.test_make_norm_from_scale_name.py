def test_make_norm_from_scale_name():
    logitnorm = mcolors.make_norm_from_scale(
        mscale.LogitScale, mcolors.Normalize)
    assert logitnorm.__name__ == "LogitScaleNorm"
