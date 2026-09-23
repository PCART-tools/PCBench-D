def get_dynamic_dims(shape):
    dynamic_dims = []

    for i, s in enumerate(shape):
        if s == -1:
            dynamic_dims.append(i)

    return dynamic_dims
