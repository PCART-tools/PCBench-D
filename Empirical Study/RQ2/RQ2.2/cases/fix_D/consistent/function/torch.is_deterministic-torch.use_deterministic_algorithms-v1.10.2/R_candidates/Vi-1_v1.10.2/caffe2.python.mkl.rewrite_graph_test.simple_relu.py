def simple_relu():
    model = ModelHelper(name="r")
    brew.relu(model, "data", "fc")
    return model, [(1, 10)]
