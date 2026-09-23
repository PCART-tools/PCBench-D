def _predict(model, x):
    return model.predict(x)[:, None]
