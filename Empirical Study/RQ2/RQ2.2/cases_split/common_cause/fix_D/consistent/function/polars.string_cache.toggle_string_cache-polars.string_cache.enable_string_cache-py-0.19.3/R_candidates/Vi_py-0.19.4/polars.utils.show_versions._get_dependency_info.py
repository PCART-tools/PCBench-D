def _get_dependency_info() -> dict[str, str]:
    # see the list of dependencies in pyproject.toml
    opt_deps = [
        "adbc_driver_sqlite",
        "cloudpickle",
        "connectorx",
        "deltalake",
        "fsspec",
        "gevent",
        "matplotlib",
        "numpy",
        "openpyxl",
        "pandas",
        "pyarrow",
        "pydantic",
        "pyiceberg",
        "pyxlsb",
        "sqlalchemy",
        "xlsx2csv",
        "xlsxwriter",
    ]
    return {f"{name}:": _get_dependency_version(name) for name in opt_deps}
