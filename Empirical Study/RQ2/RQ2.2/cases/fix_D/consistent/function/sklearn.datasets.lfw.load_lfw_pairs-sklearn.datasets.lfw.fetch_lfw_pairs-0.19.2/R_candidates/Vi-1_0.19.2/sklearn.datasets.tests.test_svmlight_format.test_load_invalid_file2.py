@raises(ValueError)
def test_load_invalid_file2():
    load_svmlight_files([datafile, invalidfile, datafile])
