def test_stem_args():
    fig, ax = plt.subplots()

    x = list(range(10))
    y = list(range(10))

    # Test the call signatures
    ax.stem(y)
    ax.stem(x, y)
    ax.stem(x, y, linefmt='r--')
    ax.stem(x, y, linefmt='r--', basefmt='b--')
