def is_ignored_only(output):
    try:
        report = cmc.parse(output)
    except cmc.ParseError:
        # in case the simple parser fails parsing the output of cuda memcheck
        # then this error is never ignored.
        return False
    count_ignored_errors = 0
    for e in report.errors:
        if 'libcublas' in ''.join(e.stack) or 'libcudnn' in ''.join(e.stack) or 'libcufft' in ''.join(e.stack):
            count_ignored_errors += 1
    return count_ignored_errors == report.num_errors
