def test_imread_with_custom_function():
    def imread2(fn):
        return np.ones((2, 3, 4), dtype='i1')
    with random_images(4, (5, 6, 3)) as globstring:
        im = da_imread(globstring, imread=imread2)
        assert (im.compute() == np.ones((4, 2, 3, 4), dtype='i1')).all()
