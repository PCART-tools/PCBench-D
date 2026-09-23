@pytest.mark.parametrize(
    "n_samples",
    [[5, 3, 0],
     np.array([5, 3, 0]),
     tuple([5, 3, 0])]
)
def test_make_blobs_n_samples_centers_none(n_samples):
    centers = None
    X, y = make_blobs(n_samples=n_samples, centers=centers, random_state=0)

    assert X.shape == (sum(n_samples), 2), "X shape mismatch"
    assert all(np.bincount(y, minlength=len(n_samples)) == n_samples), \
        "Incorrect number of samples per blob"
