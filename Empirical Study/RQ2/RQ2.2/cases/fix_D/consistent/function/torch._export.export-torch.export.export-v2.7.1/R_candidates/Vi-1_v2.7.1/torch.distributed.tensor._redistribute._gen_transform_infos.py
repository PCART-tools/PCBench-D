@cache
def _gen_transform_infos(
    src_spec: DTensorSpec,
    dst_spec: DTensorSpec,
) -> list[_TransformInfo]:
    return _gen_transform_infos_non_cached(src_spec, dst_spec)
