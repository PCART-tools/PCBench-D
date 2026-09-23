def predict(model, x):
    """ Predict with a scikit learn model

    Parameters
    ----------
    model : scikit learn classifier
    x : dask Array

    See docstring for ``da.learn.fit``
    """
    assert x.ndim == 2
    if len(x.chunks[1]) > 1:
        x = x.reblock(chunks=(x.chunks[0], sum(x.chunks[1])))
    func = partial(_predict, model)
    xx = np.zeros((1, x.shape[1]), dtype=x.dtype)
    dt = model.predict(xx).dtype
    return x.map_blocks(func, chunks=(x.chunks[0], (1,)), dtype=dt).squeeze()
