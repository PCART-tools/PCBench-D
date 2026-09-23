@raises(IOError)
def test_load_empty_lfw_pairs():
    fetch_lfw_pairs(data_home=SCIKIT_LEARN_EMPTY_DATA,
                    download_if_missing=False)
