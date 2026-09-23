def test_dot_graph_no_filename(tmpdir):
    # Map from format extension to expected return type.
    result_types = {
        'png': Image,
        'jpeg': Image,
        'dot': type(None),
        'pdf': type(None),
        'svg': SVG,
    }
    for format in result_types:
        before = tmpdir.listdir()
        result = dot_graph(dsk, filename=None, format=format)
        # We shouldn't write any files if filename is None.
        after = tmpdir.listdir()
        assert before == after
        assert isinstance(result, result_types[format])
