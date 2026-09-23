def main() -> None:
    for line in sys.stdin:
        # Convert all quoted includes to angle brackets
        match = QUOTE_INCLUDE_RE.match(line)
        if match is not None:
            print(f"#include <{match.group(1)}>{line[match.end(0):]}", end='')
            continue

        match = ANGLE_INCLUDE_RE.match(line)
        if match is not None:
            path = f"<{match.group(1)}>"
            new_path = STD_C_HEADER_MAP.get(path, path)
            tail = line[match.end(0):]
            if len(tail) > 1:
                tail = ' ' + tail
            print(f"#include {new_path}{tail}", end='')
            continue

        print(line, end='')
