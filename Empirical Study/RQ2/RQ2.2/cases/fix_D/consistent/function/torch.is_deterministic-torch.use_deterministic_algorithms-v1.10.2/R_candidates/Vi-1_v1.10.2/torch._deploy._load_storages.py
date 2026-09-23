def _load_storages(id, zip_reader, obj_bytes, serialized_storages):

    def persistent_load(saved_id):
        assert isinstance(saved_id, tuple)
        typename = _maybe_decode_ascii(saved_id[0])
        data = saved_id[1:]

        if typename == 'storage':
            return serialized_storages[data[0]]

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
