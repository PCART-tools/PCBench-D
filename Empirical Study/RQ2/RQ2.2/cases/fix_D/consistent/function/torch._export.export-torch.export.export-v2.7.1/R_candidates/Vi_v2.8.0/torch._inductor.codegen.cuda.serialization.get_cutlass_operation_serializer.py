@functools.lru_cache(1)
def get_cutlass_operation_serializer() -> Optional[CUTLASSOperationSerializer]:
    if not try_import_cutlass():
        return None
    return CUTLASSOperationSerializer()
