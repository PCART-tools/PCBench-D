def test_quiver_number_of_args():
    X = [1, 2]
    with pytest.raises(
            TypeError,
            match='takes 2-5 positional arguments but 1 were given'):
        plt.quiver(X)
    with pytest.raises(
            TypeError,
            match='takes 2-5 positional arguments but 6 were given'):
        plt.quiver(X, X, X, X, X, X)
