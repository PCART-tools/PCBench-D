def test_fit():
    sgd = SGDClassifier()

    sgd = da.learn.fit(sgd, X, Y, get=dask.get, classes=np.array([-1, 0, 1]))

    sol = sgd.predict(z)
    result = da.learn.predict(sgd, Z)
    assert result.chunks == ((2, 2),)
    assert result.compute(get=dask.get).tolist() == sol.tolist()
