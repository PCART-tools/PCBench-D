def main() -> int:
    # mimic git grep exit code behavior
    exit_code = 1
    for line in fileinput.input():
        stripped = line.rstrip()
        if not correct_trailing_newlines(stripped):
            exit_code = 0
            print(stripped)
    return exit_code
