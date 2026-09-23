def test_dot_graph_defaults():
    # Test with default args.
    default_name = 'mydask'
    default_format = 'png'
    target = '.'.join([default_name, default_format])

    ensure_not_exists(target)
    try:
        result = dot_graph(dsk)
        assert os.path.isfile(target)
        assert isinstance(result, Image)
    finally:
        ensure_not_exists(target)
