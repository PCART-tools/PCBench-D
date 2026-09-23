def simple_mlp():
    model = ModelHelper(name="r")
    brew.relu(
        model,
        brew.fc(
            model,
            brew.relu(
                model,
                brew.fc(
                    model,
                    "data",
                    "fc1",
                    10,
                    10),
                "rl1"),
            "fc2",
            10,
            10),
        "rl2")
    return model, [(1, 10)]
