def test_context():
    cfg = Config(x=1)
    with cfg(x=2) as c:
        assert c.x == 2
        c.x = 3
        assert cfg.x == 3
    assert cfg.x == 1

    with cfg(x=2) as c:
        assert c == cfg
        assert cfg.x == 2
        with cfg(x=3) as c2:
            assert c2 == cfg
            assert cfg.x == 3
            with pytest.raises(RuntimeError, match="context manager without"):
                with cfg as c3:  # Forgot to call `cfg(...)`
                    pass
            assert cfg.x == 3
        assert cfg.x == 2
    assert cfg.x == 1

    c = cfg(x=4)  # Not yet as context (not recommended, but possible)
    assert c == cfg
    assert cfg.x == 4
    # Cheat by looking at internal data; context stack should only grow with __enter__
    assert cfg._prev is not None
    assert cfg._context_stack == []
    with c:
        assert c == cfg
        assert cfg.x == 4
    assert cfg.x == 1
    # Cheat again; there was no preceding `cfg(...)` call this time
    assert cfg._prev is None
    with pytest.raises(RuntimeError, match="context manager without"):
        with cfg:
            pass
    assert cfg.x == 1
