def test_load_fake_lfw_pairs():
    lfw_pairs_train = fetch_lfw_pairs(data_home=SCIKIT_LEARN_DATA,
                                      download_if_missing=False)

    # The data is croped around the center as a rectangular bounding box
    # around the face. Colors are converted to gray levels:
    assert_equal(lfw_pairs_train.pairs.shape, (10, 2, 62, 47))

    # the target is whether the person is the same or not
    assert_array_equal(lfw_pairs_train.target, [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])

    # names of the persons can be found using the target_names array
    expected_classes = ['Different persons', 'Same person']
    assert_array_equal(lfw_pairs_train.target_names, expected_classes)

    # It is possible to ask for the original data without any croping or color
    # conversion
    lfw_pairs_train = fetch_lfw_pairs(data_home=SCIKIT_LEARN_DATA, resize=None,
                                      slice_=None, color=True,
                                      download_if_missing=False)
    assert_equal(lfw_pairs_train.pairs.shape, (10, 2, 250, 250, 3))

    # the ids and class names are the same as previously
    assert_array_equal(lfw_pairs_train.target, [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
    assert_array_equal(lfw_pairs_train.target_names, expected_classes)
