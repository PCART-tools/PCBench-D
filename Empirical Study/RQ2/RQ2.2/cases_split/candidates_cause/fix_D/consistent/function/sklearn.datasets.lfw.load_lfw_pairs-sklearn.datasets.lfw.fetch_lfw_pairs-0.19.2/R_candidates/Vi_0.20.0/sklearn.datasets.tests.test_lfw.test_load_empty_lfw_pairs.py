def test_load_empty_lfw_pairs():
    assert_raises(IOError, fetch_lfw_pairs,
                  data_home=SCIKIT_LEARN_EMPTY_DATA,
                  download_if_missing=False)
