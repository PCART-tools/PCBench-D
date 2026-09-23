def _deserialize(backend_name, obj, location):
    if backend_name == "privateuse1":
        backend_name = torch._C._get_privateuse1_backend_name()
    if location.startswith(backend_name):
        device = _validate_device(location, backend_name)
        return obj.to(device=device)
