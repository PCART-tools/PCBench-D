def test_imread():
    with random_images(4, (5, 6, 3)) as globstring:
        im = da_imread(globstring)
        assert im.shape == (4, 5, 6, 3)
        assert im.chunks == ((1, 1, 1, 1), (5,), (6,), (3,))
        assert im.dtype == 'uint8'

        assert im.compute().shape == (4, 5, 6, 3)
        assert im.compute().dtype == 'uint8'
