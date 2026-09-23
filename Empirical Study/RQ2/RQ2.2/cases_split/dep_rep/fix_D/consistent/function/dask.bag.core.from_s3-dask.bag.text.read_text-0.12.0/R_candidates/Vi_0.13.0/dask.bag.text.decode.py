def decode(block, encoding, errors):
    text = block.decode(encoding, errors)
    lines = io.StringIO(text)
    return list(lines)
