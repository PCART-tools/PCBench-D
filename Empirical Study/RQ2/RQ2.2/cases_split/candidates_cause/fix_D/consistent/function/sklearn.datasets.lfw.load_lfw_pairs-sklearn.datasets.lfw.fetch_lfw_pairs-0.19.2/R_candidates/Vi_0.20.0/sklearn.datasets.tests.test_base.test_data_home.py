def test_data_home(data_home):
    # get_data_home will point to a pre-existing folder
    data_home = get_data_home(data_home=data_home)
    assert_equal(data_home, data_home)
    assert_true(os.path.exists(data_home))

    # clear_data_home will delete both the content and the folder it-self
    clear_data_home(data_home=data_home)
    assert_false(os.path.exists(data_home))

    # if the folder is missing it will be created again
    data_home = get_data_home(data_home=data_home)
    assert_true(os.path.exists(data_home))
