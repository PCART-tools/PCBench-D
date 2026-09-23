def _load_pandas_categorical(file_name=None, model_str=None):
    pandas_key = 'pandas_categorical:'
    offset = -len(pandas_key)
    if file_name is not None:
        max_offset = -getsize(file_name)
        with open(file_name, 'rb') as f:
            while True:
                if offset < max_offset:
                    offset = max_offset
                f.seek(offset, SEEK_END)
                lines = f.readlines()
                if len(lines) >= 2:
                    break
                offset *= 2
        last_line = lines[-1].decode('utf-8').strip()
        if not last_line.startswith(pandas_key):
            last_line = lines[-2].decode('utf-8').strip()
    elif model_str is not None:
        idx = model_str.rfind('\n', 0, offset)
        last_line = model_str[idx:].strip()
    if last_line.startswith(pandas_key):
        return json.loads(last_line[len(pandas_key):])
    else:
        return None
