def correct_trailing_newlines(filename: str) -> bool:
    with open(filename, "rb") as f:
        a = len(f.read(2))
        if a == 0:
            return True
        elif a == 1:
            # file is wrong whether or not the only byte is a newline
            return False
        else:
            f.seek(-2, os.SEEK_END)
            b, c = f.read(2)
            # no ASCII byte is part of any non-ASCII character in UTF-8
            return b != NEWLINE and c == NEWLINE
