def _load_storages(id, zip_reader, obj_bytes, serialized_storages, serialized_dtypes):

    def persistent_load(saved_id):
        assert isinstance(saved_id, tuple)
        typename = _maybe_decode_ascii(saved_id[0])
        data = saved_id[1:]

        if typename == 'storage':
            # TODO: Once we decide to break serialization FC, we can
            # stop wrapping with _TypedStorage
            storage = serialized_storages[data[0]]
            dtype = serialized_dtypes[data[0]]
            return torch.storage._TypedStorage(
                wrap_storage=storage._untyped(),
                dtype=dtype)

        if typename == 'reduce_deploy':
            reduce_id, func, args = data
            if reduce_id not in _loaded_reduces:
                _loaded_reduces[reduce_id] = func(_raw_packages[zip_reader], *args)
            return _loaded_reduces[reduce_id]

        return None


    importer: Importer
    if zip_reader is not None:
        importer = OrderedImporter(_get_package(zip_reader), sys_importer)
    else:
        importer = sys_importer

    unpickler = PackageUnpickler(importer, io.BytesIO(obj_bytes))
    unpickler.persistent_load = persistent_load
    result = _deploy_objects[id] = unpickler.load()
    return result
