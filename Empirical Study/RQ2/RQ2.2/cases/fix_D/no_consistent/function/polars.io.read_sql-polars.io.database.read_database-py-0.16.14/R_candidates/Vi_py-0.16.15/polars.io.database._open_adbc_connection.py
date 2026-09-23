def _open_adbc_connection(connection_uri: str) -> Any:
    if connection_uri.startswith("sqlite"):
        try:
            import adbc_driver_sqlite.dbapi as adbc  # type: ignore[import]
        except ImportError:
            raise ImportError(
                "ADBC sqlite driver not detected. Please run `pip install "
                "adbc_driver_sqlite`."
            ) from None
        connection_uri = connection_uri.replace(r"sqlite:///", "")
    elif connection_uri.startswith("postgres"):
        try:
            import adbc_driver_postgresql.dbapi as adbc  # type: ignore[import]
        except ImportError:
            raise ImportError(
                "ADBC postgresql driver not detected. Please run `pip install "
                "adbc_driver_postgresql`."
            ) from None
    else:
        raise ValueError("ADBC does not currently support this database.")
    return adbc.connect(connection_uri)
