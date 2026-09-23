def _save(obj, zip_file, pickle_module, pickle_protocol):
    serialized_storages = {}
    id_map: Dict[int, str] = {}

    def persistent_id(obj):
        # FIXME: the docs say that persistent_id should only return a string
        # but torch store returns tuples. This works only in the binary protocol
        # see
        # https://docs.python.org/2/library/pickle.html#pickling-and-unpickling-external-objects
        # https://github.com/python/cpython/blob/master/Lib/pickle.py#L527-L537
        if torch.is_storage(obj):
            storage_type = normalize_storage_type(type(obj))
            obj_key = id_map.setdefault(obj._cdata, str(len(id_map)))
            location = location_tag(obj)
            serialized_storages[obj_key] = obj

            return ('storage',
                    storage_type,
                    obj_key,
                    location,
                    obj.size())
        return None

    # Write the pickle data for `obj`
    data_buf = io.BytesIO()
    pickler = pickle_module.Pickler(data_buf, protocol=pickle_protocol)
    pickler.persistent_id = persistent_id
    pickler.dump(obj)
    data_value = data_buf.getvalue()
    zip_file.write_record('data.pkl', data_value, len(data_value))

    # Write each tensor to a file named tensor/the_tensor_key in the zip archive
    for key in sorted(serialized_storages.keys()):
        name = f'data/{key}'
        storage = serialized_storages[key]
        # given that we copy things around anyway, we might use storage.cpu()
        # this means to that to get tensors serialized, you need to implement
        # .cpu() on the underlying Storage
        if storage.device.type != 'cpu':
            storage = storage.cpu()
        # Now that it is on the CPU we can directly copy it into the zip file
        num_bytes = storage.size() * storage.element_size()
        zip_file.write_record(name, storage.data_ptr(), num_bytes)
