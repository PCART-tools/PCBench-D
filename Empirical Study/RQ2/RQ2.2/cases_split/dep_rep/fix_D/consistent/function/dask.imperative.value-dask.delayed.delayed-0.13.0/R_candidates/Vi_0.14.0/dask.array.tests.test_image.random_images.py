@contextmanager
def random_images(n, shape):
    with tmpdir() as dirname:
        for i in range(n):
            fn = os.path.join(dirname, 'image.%d.png' % i)
            x = np.random.randint(0, 255, size=shape).astype('i1')
            imsave(fn, x)

        yield os.path.join(dirname, '*.png')
