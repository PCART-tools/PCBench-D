def test_load_empty_lfw_people():
    assert_raises(IOError, fetch_lfw_people, data_home=SCIKIT_LEARN_EMPTY_DATA,
                  download_if_missing=False)
