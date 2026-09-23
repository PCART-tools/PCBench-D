def _get_weights(model, namescope=None):
    if namescope is None:
        namescope = scope.CurrentNameScope()

    if namescope == '':
        return model.weights[:]
    else:
        return [w for w in model.weights if w.GetNameScope() == namescope]
