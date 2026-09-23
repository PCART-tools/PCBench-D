def _get_closure_vars():
    global _CLOSURE_VARS
    if _CLOSURE_VARS is None:
        _CLOSURE_VARS = {
            "___check_type_id": check_type_id,
            "___check_obj_id": check_obj_id,
            "___odict_getitem": collections.OrderedDict.__getitem__,
            "___key_to_id": key_to_id,
            "___dict_version": dict_version,
            "___dict_contains": lambda a, b: dict.__contains__(b, a),
            "___tuple_iterator_len": tuple_iterator_len,
            "___normalize_range_iter": normalize_range_iter,
            "___tuple_iterator_getitem": tuple_iterator_getitem,
            "___get_torch_function_mode_stack_at": get_torch_function_mode_stack_at,
            "__math_isnan": math.isnan,
            "__numpy_isnan": None if np is None else np.isnan,
            "inf": float("inf"),
            "__load_module": importlib.import_module,
            "utils_device": torch.utils._device,
            "device": torch.device,
            "___from_numpy": from_numpy,
            "___as_tensor": torch._as_tensor_fullprec,
            "torch": torch,
            "inspect": inspect,
        }
    return _CLOSURE_VARS
