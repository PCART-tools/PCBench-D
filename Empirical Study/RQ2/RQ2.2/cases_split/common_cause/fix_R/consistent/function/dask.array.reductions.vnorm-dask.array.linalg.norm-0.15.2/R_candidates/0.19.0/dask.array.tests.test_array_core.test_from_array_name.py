def test_from_array_name():
    x = np.array([1, 2, 3, 4, 5])
    chunks = x.shape
    # Default is tokenize the array
    dx = da.from_array(x, chunks=chunks)
    hashed_name = dx.name
    assert da.from_array(x, chunks=chunks).name == hashed_name
    # Specify name directly
    assert da.from_array(x, chunks=chunks, name='x').name == 'x'
    # False gives a random name
    dx2 = da.from_array(x, chunks=chunks, name=False)
    dx3 = da.from_array(x, chunks=chunks, name=False)
    assert dx2.name != hashed_name
    assert dx3.name != hashed_name
    assert dx2.name != dx3.name
