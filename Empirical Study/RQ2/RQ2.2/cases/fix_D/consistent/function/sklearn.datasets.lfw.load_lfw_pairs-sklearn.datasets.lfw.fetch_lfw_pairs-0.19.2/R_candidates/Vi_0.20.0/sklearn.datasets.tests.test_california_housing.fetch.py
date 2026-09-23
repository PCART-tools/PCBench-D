def fetch(*args, **kwargs):
    return fetch_california_housing(*args, download_if_missing=False, **kwargs)
