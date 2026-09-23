def vec_isa_ok_default() -> Optional[bool]:
    if os.environ.get("TORCHINDUCTOR_VEC_ISA_OK") == "1":
        return True
    if os.environ.get("TORCHINDUCTOR_VEC_ISA_OK") == "0":
        return False
    return None
