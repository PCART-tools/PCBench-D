def test_raise_on_meta_error():
    try:
        with raise_on_meta_error():
            raise RuntimeError("Bad stuff")
    except Exception as e:
        assert e.args[0].startswith("Metadata inference failed.\n")
        assert 'RuntimeError' in e.args[0]

    try:
        with raise_on_meta_error("myfunc"):
            raise RuntimeError("Bad stuff")
    except Exception as e:
        assert e.args[0].startswith("Metadata inference failed in `myfunc`.\n")
        assert 'RuntimeError' in e.args[0]
