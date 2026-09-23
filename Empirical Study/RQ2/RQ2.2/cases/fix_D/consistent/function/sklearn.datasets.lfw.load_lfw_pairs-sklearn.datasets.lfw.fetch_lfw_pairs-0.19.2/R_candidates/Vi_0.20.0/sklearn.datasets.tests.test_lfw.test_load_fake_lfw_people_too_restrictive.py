def test_load_fake_lfw_people_too_restrictive():
    assert_raises(ValueError, fetch_lfw_people, data_home=SCIKIT_LEARN_DATA,
                  min_faces_per_person=100, download_if_missing=False)
