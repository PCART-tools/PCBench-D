def predict(model, x):
    """ Predict with a scikit learn model

    Parameters
    ----------

    model: scikit learn classifier
    x: dask Array

    See docstring for ``da.learn.fit``
    """
    assert x.ndim == 2
    if len(x.chunks[1]) > 1:
        x = x.reblock(chunks=(x.chunks[0], sum(x.chunks[1])))
    func = partial(_predict, model)
    return x.map_blocks(func, chunks=(x.chunks[0], (1,))).squeeze()
