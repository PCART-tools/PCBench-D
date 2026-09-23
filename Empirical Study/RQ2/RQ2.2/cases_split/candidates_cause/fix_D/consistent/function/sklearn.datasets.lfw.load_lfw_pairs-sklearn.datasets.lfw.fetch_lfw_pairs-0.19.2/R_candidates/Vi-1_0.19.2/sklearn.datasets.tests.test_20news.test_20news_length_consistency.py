def test_20news_length_consistency():
    """Checks the length consistencies within the bunch

    This is a non-regression test for a bug present in 0.16.1.
    """
    try:
        data = datasets.fetch_20newsgroups(
            subset='all', download_if_missing=False, shuffle=False)
    except IOError:
        raise SkipTest("Download 20 newsgroups to run this test")
    # Extract the full dataset
    data = datasets.fetch_20newsgroups(subset='all')
    assert_equal(len(data['data']), len(data.data))
    assert_equal(len(data['target']), len(data.target))
    assert_equal(len(data['filenames']), len(data.filenames))
