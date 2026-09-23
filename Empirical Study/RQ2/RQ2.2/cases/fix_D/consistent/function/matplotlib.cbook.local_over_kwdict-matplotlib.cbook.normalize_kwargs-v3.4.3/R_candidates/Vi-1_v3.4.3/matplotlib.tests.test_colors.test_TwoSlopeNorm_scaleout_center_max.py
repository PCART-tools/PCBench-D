def test_TwoSlopeNorm_scaleout_center_max():
    # test the vmax never goes below vcenter
    norm = mcolors.TwoSlopeNorm(vcenter=0)
    norm([-1, -2, -3, -5])
    assert norm.vmax == 0
    assert norm.vmin == -5
