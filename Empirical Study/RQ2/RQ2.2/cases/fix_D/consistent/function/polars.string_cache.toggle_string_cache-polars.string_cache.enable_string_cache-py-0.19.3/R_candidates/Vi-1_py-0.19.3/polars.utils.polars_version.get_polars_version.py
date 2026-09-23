def get_polars_version() -> str:
    """
    Return the version of the Python Polars package as a string.

    If the Polars binary is missing, returns an empty string.
    """
    return polars_version_string
