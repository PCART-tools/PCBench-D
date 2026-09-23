def executor_test_model_names():
    if hu.is_sandcastle() or hu.is_travis():
        return ["MLP"]
    else:
        return sorted(conv_model_generators().keys())
