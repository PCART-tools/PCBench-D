def get_categorical_limit(record):
    key = get_key(record)
    return key.metadata.categorical_limit
