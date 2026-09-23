@pytest.mark.skipif("not bokeh")
def test_saves_file():
    with tmpfile('html') as fn:
        with prof:
            get(dsk, 'e')
        # Run just to see that it doesn't error
        prof.visualize(show=False, file_path=fn)

        assert os.path.exists(fn)
        with open(fn) as f:
            assert 'html' in f.read().lower()
