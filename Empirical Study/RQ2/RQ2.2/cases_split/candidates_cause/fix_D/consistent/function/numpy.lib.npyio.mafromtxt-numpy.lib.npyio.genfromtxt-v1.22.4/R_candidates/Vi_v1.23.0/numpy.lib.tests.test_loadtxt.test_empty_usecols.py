def test_empty_usecols():
    txt = StringIO("0,0,XXX\n0,XXX,0,XXX\n0,XXX,XXX,0,XXX\n")
    res = np.loadtxt(txt, dtype=np.dtype([]), delimiter=",", usecols=[])
    assert res.shape == (3,)
    assert res.dtype == np.dtype([])
