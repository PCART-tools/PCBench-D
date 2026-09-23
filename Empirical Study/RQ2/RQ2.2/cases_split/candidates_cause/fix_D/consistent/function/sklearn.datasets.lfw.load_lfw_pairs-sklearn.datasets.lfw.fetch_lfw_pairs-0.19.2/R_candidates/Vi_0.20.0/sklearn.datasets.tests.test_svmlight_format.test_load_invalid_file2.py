def test_load_invalid_file2():
    assert_raises(ValueError, load_svmlight_files,
                  [datafile, invalidfile, datafile])
