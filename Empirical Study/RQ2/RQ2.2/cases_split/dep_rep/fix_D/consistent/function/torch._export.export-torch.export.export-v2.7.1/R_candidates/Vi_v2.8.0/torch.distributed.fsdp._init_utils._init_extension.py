@no_type_check
def _init_extension(state: _FSDPState, device_mesh: DeviceMesh = None) -> _FSDPState:
    # TODO: we need to add additional check once we support FSDP + PiPPy.
    # This check is currently sufficient, since we only support FSDP + TP.
    root_mesh = _mesh_resources.get_root_mesh(device_mesh)
    # if a root mesh is not the same as device_mesh,
    # meaning the device_mesh is sliced out from the root mesh.
    if device_mesh and root_mesh != state._device_mesh:
        state._fsdp_extension = DTensorExtensions(state._device_handle)
    else:
        # We need to explicitly set _fsdp_extension to None.
        # Otherwise, we will run into an infinite recursion when getting the attribute.
        state._fsdp_extension = None
    return state
