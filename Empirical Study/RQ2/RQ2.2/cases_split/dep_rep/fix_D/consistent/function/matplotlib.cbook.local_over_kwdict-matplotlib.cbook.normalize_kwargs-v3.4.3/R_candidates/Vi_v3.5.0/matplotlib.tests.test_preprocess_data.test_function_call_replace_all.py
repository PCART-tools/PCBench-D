def test_function_call_replace_all():
    """Test without a "replace_names" argument, all vars should be replaced."""
    data = {"a": [1, 2], "b": [8, 9], "x": "xyz"}

    @_preprocess_data(label_namer="y")
    def func_replace_all(ax, x, y, ls="x", label=None, w="NOT"):
        return "x: %s, y: %s, ls: %s, w: %s, label: %s" % (
            list(x), list(y), ls, w, label)

    assert (func_replace_all(None, "a", "b", w="x", data=data) ==
            "x: [1, 2], y: [8, 9], ls: x, w: xyz, label: b")
    assert (func_replace_all(None, x="a", y="b", w="x", data=data) ==
            "x: [1, 2], y: [8, 9], ls: x, w: xyz, label: b")
    assert (func_replace_all(None, "a", "b", w="x", label="", data=data) ==
            "x: [1, 2], y: [8, 9], ls: x, w: xyz, label: ")
    assert (
        func_replace_all(None, "a", "b", w="x", label="text", data=data) ==
        "x: [1, 2], y: [8, 9], ls: x, w: xyz, label: text")
    assert (
        func_replace_all(None, x="a", y="b", w="x", label="", data=data) ==
        "x: [1, 2], y: [8, 9], ls: x, w: xyz, label: ")
    assert (
        func_replace_all(None, x="a", y="b", w="x", label="text", data=data) ==
        "x: [1, 2], y: [8, 9], ls: x, w: xyz, label: text")
