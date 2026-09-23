def test_rvgeneric_std():
    # Regression test for #1191
    assert_array_almost_equal(stats.t.std([5, 6]), [1.29099445, 1.22474487])
