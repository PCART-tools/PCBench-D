def test_lazy_import_nonbuiltins():
    sp = lazy._lazy_import("scipy")
    np = lazy._lazy_import("numpy")
    if isinstance(sp, lazy.DelayedImportErrorModule):
        try:
            sp.pi
            assert False
        except ModuleNotFoundError:
            pass
    elif isinstance(np, lazy.DelayedImportErrorModule):
        try:
            np.sin(np.pi)
            assert False
        except ModuleNotFoundError:
            pass
    else:
        assert np.sin(sp.pi) == pytest.approx(0, 1e-6)
