def test_python2_python3_interoperability():
    fname = 'win64python2.npy'
    path = os.path.join(os.path.dirname(__file__), 'data', fname)
    data = np.load(path)
    assert_array_equal(data, np.ones(2))
