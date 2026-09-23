def test_load_fake_lfw_people():
    lfw_people = fetch_lfw_people(data_home=SCIKIT_LEARN_DATA,
                                  min_faces_per_person=3,
                                  download_if_missing=False)

    # The data is croped around the center as a rectangular bounding box
    # around the face. Colors are converted to gray levels:
    assert_equal(lfw_people.images.shape, (10, 62, 47))
    assert_equal(lfw_people.data.shape, (10, 2914))

    # the target is array of person integer ids
    assert_array_equal(lfw_people.target, [2, 0, 1, 0, 2, 0, 2, 1, 1, 2])

    # names of the persons can be found using the target_names array
    expected_classes = ['Abdelatif Smith', 'Abhati Kepler', 'Onur Lopez']
    assert_array_equal(lfw_people.target_names, expected_classes)

    # It is possible to ask for the original data without any croping or color
    # conversion and not limit on the number of picture per person
    lfw_people = fetch_lfw_people(data_home=SCIKIT_LEARN_DATA, resize=None,
                                  slice_=None, color=True,
                                  download_if_missing=False)
    assert_equal(lfw_people.images.shape, (17, 250, 250, 3))

    # the ids and class names are the same as previously
    assert_array_equal(lfw_people.target,
                       [0, 0, 1, 6, 5, 6, 3, 6, 0, 3, 6, 1, 2, 4, 5, 1, 2])
    assert_array_equal(lfw_people.target_names,
                       ['Abdelatif Smith', 'Abhati Kepler', 'Camara Alvaro',
                        'Chen Dupont', 'John Lee', 'Lin Bauman', 'Onur Lopez'])

    # test return_X_y option
    fetch_func = partial(fetch_lfw_people, data_home=SCIKIT_LEARN_DATA,
                         resize=None,
                         slice_=None, color=True,
                         download_if_missing=False)
    check_return_X_y(lfw_people, fetch_func)
