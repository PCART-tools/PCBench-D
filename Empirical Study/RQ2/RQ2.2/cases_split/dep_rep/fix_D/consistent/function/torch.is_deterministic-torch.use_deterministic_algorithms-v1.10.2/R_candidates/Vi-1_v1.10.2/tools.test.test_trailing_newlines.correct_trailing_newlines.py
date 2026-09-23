def correct_trailing_newlines(file_contents: str) -> bool:
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        filename = tmp.name
        tmp.write(file_contents)
    return trailing_newlines.correct_trailing_newlines(filename)
