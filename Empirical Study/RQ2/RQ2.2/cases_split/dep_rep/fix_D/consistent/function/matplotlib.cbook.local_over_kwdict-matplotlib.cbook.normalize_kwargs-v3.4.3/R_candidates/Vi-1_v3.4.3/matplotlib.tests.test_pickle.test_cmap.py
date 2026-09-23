@pytest.mark.parametrize("cmap", cm._cmap_registry.values())
def test_cmap(cmap):
    pickle.dumps(cmap)
