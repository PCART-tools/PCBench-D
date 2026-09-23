def _get_dt_pg(dt: DTensor) -> c10d.ProcessGroup:
    mesh = dt.device_mesh
    assert mesh.ndim == 1, "Only 1D DeviceMeshes currently handled"
    return mesh.get_group()
