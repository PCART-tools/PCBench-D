def double_matmul():
    model = ModelHelper(name="r")
    fc0 = brew.fc(model, "data", "fc0", 10, 10)
    fc1 = brew.fc(model, fc0, "fc1", 10, 10)
    model.Proto().external_output[:] = [str(fc0), str(fc1)]
    return model, [(1, 10)]
