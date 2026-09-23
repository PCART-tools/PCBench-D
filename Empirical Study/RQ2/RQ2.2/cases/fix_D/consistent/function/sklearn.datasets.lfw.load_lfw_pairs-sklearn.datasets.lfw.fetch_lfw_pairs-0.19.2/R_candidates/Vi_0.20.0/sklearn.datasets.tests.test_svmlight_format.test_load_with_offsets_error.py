def test_load_with_offsets_error():
    assert_raises_regex(ValueError, "n_features is required",
                        load_svmlight_file, datafile, offset=3, length=3)
