def _get_dask_client(client: Optional[Client]) -> Client:
    """Choose a Dask client to use.

    Parameters
    ----------
    client : dask.distributed.Client or None
        Dask client.

    Returns
    -------
    client : dask.distributed.Client
        A Dask client.
    """
    if client is None:
        return default_client()
    else:
        return client
