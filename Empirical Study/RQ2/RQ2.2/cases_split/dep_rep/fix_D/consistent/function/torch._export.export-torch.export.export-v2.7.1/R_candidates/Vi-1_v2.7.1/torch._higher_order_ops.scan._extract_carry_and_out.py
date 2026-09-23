def _extract_carry_and_out(flat_out: list[Any], num_carry: int):
    return flat_out[:num_carry], flat_out[num_carry:]
