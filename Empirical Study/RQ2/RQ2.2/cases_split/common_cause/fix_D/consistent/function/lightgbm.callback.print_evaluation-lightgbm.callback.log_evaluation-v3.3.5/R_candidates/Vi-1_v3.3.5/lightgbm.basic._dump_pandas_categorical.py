def _dump_pandas_categorical(pandas_categorical, file_name=None):
    categorical_json = json.dumps(pandas_categorical, default=json_default_with_numpy)
    pandas_str = f'\npandas_categorical:{categorical_json}\n'
    if file_name is not None:
        with open(file_name, 'a') as f:
            f.write(pandas_str)
    return pandas_str
