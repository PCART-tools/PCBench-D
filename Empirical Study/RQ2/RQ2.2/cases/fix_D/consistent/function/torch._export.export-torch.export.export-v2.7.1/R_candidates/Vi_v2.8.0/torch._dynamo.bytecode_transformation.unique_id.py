def unique_id(name, with_uuid=False) -> str:
    ret = f"{name}_{next(_unique_id_counter)}"
    if with_uuid:
        ret += f"_{uuid.uuid4()}".replace("-", "_")
    return ret
