def test_lazy_import_impact_on_sys_modules():
    math = lazy._lazy_import("math")
    anything_not_real = lazy._lazy_import("anything_not_real")

    assert type(math) == types.ModuleType
    assert "math" in sys.modules
    assert type(anything_not_real) == lazy.DelayedImportErrorModule
    assert "anything_not_real" not in sys.modules

    # only do this if numpy is installed
    np_test = pytest.importorskip("numpy")
    np = lazy._lazy_import("numpy")
    assert type(np) == types.ModuleType
    assert "numpy" in sys.modules

    np.pi  # trigger load of numpy

    assert type(np) == types.ModuleType
    assert "numpy" in sys.modules
