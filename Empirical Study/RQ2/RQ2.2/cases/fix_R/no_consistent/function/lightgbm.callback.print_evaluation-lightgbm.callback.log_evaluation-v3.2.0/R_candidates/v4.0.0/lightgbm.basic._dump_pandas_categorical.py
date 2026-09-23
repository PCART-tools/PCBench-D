def _dump_pandas_categorical(
    pandas_categorical: Optional[List[List]],
    file_name: Optional[Union[str, Path]] = None
) -> str:
    categorical_json = json.dumps(pandas_categorical, default=_json_default_with_numpy)
    pandas_str = f'\npandas_categorical:{categorical_json}\n'
    if file_name is not None:
        with open(file_name, 'a') as f:
            f.write(pandas_str)
    return pandas_str
