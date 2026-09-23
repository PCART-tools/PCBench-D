def test_sensitive_to_partials():
    assert (delayed(partial(add, 10), pure=True)(2)._key !=
            delayed(partial(add, 20), pure=True)(2)._key)
