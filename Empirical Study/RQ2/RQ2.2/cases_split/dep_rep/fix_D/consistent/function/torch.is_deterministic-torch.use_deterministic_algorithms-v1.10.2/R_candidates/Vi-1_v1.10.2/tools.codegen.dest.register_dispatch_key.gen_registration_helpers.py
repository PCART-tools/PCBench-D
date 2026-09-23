def gen_registration_helpers(backend_index: BackendIndex) -> List[str]:
    return [
        *gen_create_out_helper(backend_index),
        *gen_resize_out_helper(backend_index)
    ]
