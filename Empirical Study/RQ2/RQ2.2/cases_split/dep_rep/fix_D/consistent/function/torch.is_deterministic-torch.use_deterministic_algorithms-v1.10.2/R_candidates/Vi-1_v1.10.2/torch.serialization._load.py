def _load(zip_file, map_location, pickle_module, pickle_file='data.pkl', **pickle_load_args):
    restore_location = _get_restore_location(map_location)

    loaded_storages = {}

    def load_tensor(data_type, size, key, location):
        name = f'data/{key}'
        dtype = data_type(0).dtype

        storage = zip_file.get_storage_from_record(name, size, dtype).storage()
        loaded_storages[key] = restore_location(storage, location)

    def persistent_load(saved_id):
        assert isinstance(saved_id, tuple)
        typename = _maybe_decode_ascii(saved_id[0])
        data = saved_id[1:]

        assert typename == 'storage', \
            f"Unknown typename for persistent_load, expected 'storage' but got '{typename}'"
        data_type, key, location, size = data
        if key not in loaded_storages:
            load_tensor(data_type, size, key, _maybe_decode_ascii(location))
        storage = loaded_storages[key]
        return storage

    load_module_mapping: Dict[str, str] = {
        # See https://github.com/pytorch/pytorch/pull/51633
        'torch.tensor': 'torch._tensor'
    }

    # Need to subclass Unpickler instead of directly monkey-patching the find_class method
    # because it's marked readonly in pickle.
    # The type: ignore is because mypy can't statically determine the type of this class.
    class UnpicklerWrapper(pickle_module.Unpickler):  # type: ignore[name-defined]
        # from https://stackoverflow.com/questions/13398462/unpickling-python-objects-with-a-changed-module-path/13405732
        # Lets us override the imports that pickle uses when unpickling an object.
        # This is useful for maintaining BC if we change a module path that tensor instantiation relies on.
        def find_class(self, mod_name, name):
            mod_name = load_module_mapping.get(mod_name, mod_name)
            return super().find_class(mod_name, name)

    # Load the data (which may in turn use `persistent_load` to load tensors)
    data_file = io.BytesIO(zip_file.get_record(pickle_file))

    unpickler = UnpicklerWrapper(data_file, **pickle_load_args)
    unpickler.persistent_load = persistent_load
    result = unpickler.load()

    torch._utils._validate_loaded_sparse_tensors()

    return result
