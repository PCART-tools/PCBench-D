def simple_fc():
    model = ModelHelper(name="r")
    brew.fc(model, "data", "fc", 10, 10)
    return model, [(1, 10)]
