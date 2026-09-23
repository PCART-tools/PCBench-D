def clear_data_home(data_home=None):
    """Delete all the content of the data home cache.

    Parameters
    ----------
    data_home : str | None
        The path to scikit-learn data dir.
    """
    data_home = get_data_home(data_home)
    shutil.rmtree(data_home)
