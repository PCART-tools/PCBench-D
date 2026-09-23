def _warn_if_global_cmap_modified(cmap):
    if getattr(cmap, '_global', False):
        _api.warn_deprecated(
            "3.3",
            removal="3.6",
            message="You are modifying the state of a globally registered "
                    "colormap. This has been deprecated since %(since)s and "
                    "%(removal)s, you will not be able to modify a "
                    "registered colormap in-place. To remove this warning, "
                    "you can make a copy of the colormap first. "
                    f'cmap = mpl.cm.get_cmap("{cmap.name}").copy()'
        )
