def unique_id(name) -> str:
    return f"{name}_{next(_unique_id_counter)}"
