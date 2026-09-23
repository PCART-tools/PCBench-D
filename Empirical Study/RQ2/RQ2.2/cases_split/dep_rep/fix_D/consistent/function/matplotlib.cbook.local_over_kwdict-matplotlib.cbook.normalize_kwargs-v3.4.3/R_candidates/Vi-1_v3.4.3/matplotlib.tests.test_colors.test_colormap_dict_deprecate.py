def test_colormap_dict_deprecate():
    # Make sure we warn on get and set access into cmap_d
    with pytest.warns(cbook.MatplotlibDeprecationWarning,
                      match="The global colormaps dictionary is no longer"):
        cmap = plt.cm.cmap_d['viridis']

    with pytest.warns(cbook.MatplotlibDeprecationWarning,
                      match="The global colormaps dictionary is no longer"):
        plt.cm.cmap_d['test'] = cmap
