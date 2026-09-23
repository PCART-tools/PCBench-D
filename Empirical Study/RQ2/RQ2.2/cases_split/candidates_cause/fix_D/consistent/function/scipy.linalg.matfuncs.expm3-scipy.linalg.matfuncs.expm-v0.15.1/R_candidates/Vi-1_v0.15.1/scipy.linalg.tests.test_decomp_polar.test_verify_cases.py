def test_verify_cases():
    for a in verify_cases:
        yield verify_polar, a
