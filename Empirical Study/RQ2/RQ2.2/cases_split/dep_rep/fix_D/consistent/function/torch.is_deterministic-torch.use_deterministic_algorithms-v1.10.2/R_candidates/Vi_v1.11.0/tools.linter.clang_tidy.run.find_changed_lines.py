def find_changed_lines(diff: str) -> Dict[str, List[Tuple[int, int]]]:
    # Delay import since this isn't required unless using the --diff-file
    # argument, which for local runs people don't care about
    try:
        import unidiff  # type: ignore[import]
    except ImportError as e:
        e.msg += ", run 'pip install unidiff'"  # type: ignore[attr-defined]
        raise e

    files: Any = collections.defaultdict(list)

    for file in unidiff.PatchSet(diff):
        for hunk in file:
            added_line_nos = [line.target_line_no for line in hunk if line.is_added]

            if len(added_line_nos) == 0:
                continue

            # Convert list of line numbers to ranges
            # Eg: [1, 2, 3, 12, 13, 14, 15] becomes [[1,3], [12, 15]]
            i = 1
            ranges = [[added_line_nos[0], added_line_nos[0]]]
            while i < len(added_line_nos):
                if added_line_nos[i] != added_line_nos[i - 1] + 1:
                    ranges[-1][1] = added_line_nos[i - 1]
                    ranges.append([added_line_nos[i], added_line_nos[i]])
                i += 1
            ranges[-1][1] = added_line_nos[-1]

            files[file.path] += ranges

    return dict(files)
