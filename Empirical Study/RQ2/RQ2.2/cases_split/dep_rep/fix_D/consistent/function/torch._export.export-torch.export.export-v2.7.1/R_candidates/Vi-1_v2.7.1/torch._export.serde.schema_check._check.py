def _check(x, msg):
    if not x:
        raise SchemaUpdateError(msg)
