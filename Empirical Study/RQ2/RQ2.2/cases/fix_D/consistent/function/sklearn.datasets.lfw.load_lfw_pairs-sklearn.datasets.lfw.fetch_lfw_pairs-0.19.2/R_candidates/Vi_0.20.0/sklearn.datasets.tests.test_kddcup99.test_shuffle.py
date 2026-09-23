def test_shuffle():
    try:
        dataset = fetch_kddcup99(random_state=0, subset='SA', shuffle=True,
                                 percent10=True, download_if_missing=False)
    except IOError:
        raise SkipTest("kddcup99 dataset can not be loaded.")

    assert(any(dataset.target[-100:] == b'normal.'))
