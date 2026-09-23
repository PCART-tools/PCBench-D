def test_preprocess():
    def preprocess(x):
        x[:] = 1
        return x[:, :, 0]
    with random_images(4, (2, 3, 4)) as globstring:
        im = da_imread(globstring, preprocess=preprocess)
        assert (im.compute() == np.ones((4, 2, 3), dtype='i1')).all()
