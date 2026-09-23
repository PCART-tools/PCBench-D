def _recover_record_by_prefix(names, prefix=''):
    """
    Tries to recover record by taking a subset of blob names with
    a given prefix name and interpreting them as schema column names
    """
    from caffe2.python import schema
    column_names = [name[len(prefix):] for name in names
                    if name.startswith(prefix)]
    if not column_names:
        return None
    return schema.from_column_list(
        column_names,
        col_blobs=[_get_blob_ref(prefix + name) for name in column_names])
