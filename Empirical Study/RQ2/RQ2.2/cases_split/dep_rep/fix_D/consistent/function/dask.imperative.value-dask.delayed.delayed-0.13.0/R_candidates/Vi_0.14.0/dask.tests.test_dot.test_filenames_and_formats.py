def test_filenames_and_formats():
    # Test with a variety of user provided args
    filenames = ['mydaskpdf', 'mydask.pdf', 'mydask.pdf', 'mydaskpdf', 'mydask.pdf.svg']
    formats = ['svg', None, 'svg', None, None]
    targets = ['mydaskpdf.svg', 'mydask.pdf', 'mydask.pdf.svg', 'mydaskpdf.png', 'mydask.pdf.svg']

    result_types = {
        'png': Image,
        'jpeg': Image,
        'dot': type(None),
        'pdf': type(None),
        'svg': SVG,
    }

    for filename, format, target in zip(filenames, formats, targets):
        expected_result_type = result_types[target.split('.')[-1]]
        result = dot_graph(dsk, filename=filename, format=format)
        assert os.path.isfile(target)
        assert isinstance(result, expected_result_type)
        ensure_not_exists(target)
