def test_dot_graph(tmpdir):
    # Use a name that the shell would interpret specially to ensure that we're
    # not vulnerable to shell injection when interacting with `dot`.
    filename = str(tmpdir.join('$(touch should_not_get_created.txt)'))

    # Map from format extension to expected return type.
    result_types = {
        'png': Image,
        'jpeg': Image,
        'dot': type(None),
        'pdf': type(None),
        'svg': SVG,
    }
    for format in result_types:
        target = '.'.join([filename, format])
        ensure_not_exists(target)
        try:
            result = dot_graph(dsk, filename=filename, format=format)

            assert not os.path.exists('should_not_get_created.txt')
            assert os.path.isfile(target)
            assert isinstance(result, result_types[format])
        finally:
            ensure_not_exists(target)
