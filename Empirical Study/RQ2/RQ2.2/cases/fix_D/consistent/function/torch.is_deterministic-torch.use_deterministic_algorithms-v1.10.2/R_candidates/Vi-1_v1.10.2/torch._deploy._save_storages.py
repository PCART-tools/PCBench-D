def _save_storages(importer, obj):
    serialized_storages = []
    serialized_dtypes = []

    importer = importer if isinstance(importer, torch.package.PackageImporter) else None
    importers: Importer
    if importer is not None:
        importers = OrderedImporter(importer, sys_importer)
    else:
        importers = sys_importer

    def persistent_id(obj):
        # FIXME: the docs say that persistent_id should only return a string
        # but torch store returns tuples. This works only in the binary protocol
        # see
        # https://docs.python.org/2/library/pickle.html#pickling-and-unpickling-external-objects
        # https://github.com/python/cpython/blob/master/Lib/pickle.py#L527-L537
        if torch.is_storage(obj):
            serialized_storages.append(obj)
            serialized_dtypes.append(obj.dtype)
            return ('storage', len(serialized_storages) - 1)

        if hasattr(obj, "__reduce_deploy__"):
            if _serialized_reduces.get(id(obj)) is None:
                _serialized_reduces[id(obj)] = (
                    "reduce_deploy",
                    id(obj),
                    *obj.__reduce_deploy__(importers),
                )
            return _serialized_reduces[id(obj)]

        return None

    # Write the pickle data for `obj`
    data_buf = io.BytesIO()
    pickler = create_pickler(data_buf, importers)
    pickler.persistent_id = persistent_id
    pickler.dump(obj)
    data_value = data_buf.getvalue()
    return data_value, serialized_storages, serialized_dtypes, importer.zip_reader if importer else None
