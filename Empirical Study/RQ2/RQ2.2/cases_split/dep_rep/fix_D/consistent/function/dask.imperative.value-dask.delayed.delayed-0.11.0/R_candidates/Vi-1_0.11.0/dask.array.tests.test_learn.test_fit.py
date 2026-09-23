def test_fit():
    sgd = SGDClassifier()

    sgd = da.learn.fit(sgd, X, Y, get=dask.get, classes=np.array([-1, 1]))

    result = sgd.predict(z)
    assert result.tolist() == [1, -1, 1, -1]

    result = da.learn.predict(sgd, Z)
    assert result.chunks == ((2, 2),)
    assert result.compute(get=dask.get).tolist() == [1, -1, 1, -1]
