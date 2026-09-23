def _assert_close(value1, value2, threshold, err_msg=''):
    np.testing.assert_allclose(
        value1, value2,
        atol=threshold, rtol=threshold,
        err_msg=err_msg,
    )

    delta = np.abs(value1 - value2).flatten()
    return np.mean(delta), max(delta)
