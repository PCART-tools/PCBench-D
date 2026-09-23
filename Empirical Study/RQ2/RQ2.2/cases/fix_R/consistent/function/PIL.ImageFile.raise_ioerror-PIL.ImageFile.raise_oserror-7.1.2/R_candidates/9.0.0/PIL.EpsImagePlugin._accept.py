def _accept(prefix):
    return prefix[:4] == b"%!PS" or (len(prefix) >= 4 and i32(prefix) == 0xC6D3D0C5)
