def load_lfw_pairs(download_if_missing=False, **kwargs):
    """Alias for fetch_lfw_pairs(download_if_missing=False)

    Check fetch_lfw_pairs.__doc__ for the documentation and parameter list.
    """
    return fetch_lfw_pairs(download_if_missing=download_if_missing, **kwargs)
