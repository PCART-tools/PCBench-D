def has_breakpad():
    # We always build with breakpad in CI
    if IS_IN_CI:
        return True

    # If not on a special build, check that the library was actually linked in
    try:
        torch._C._get_minidump_directory()  # type: ignore[attr-defined]
        return True
    except RuntimeError as e:
        if "Minidump handler is uninintialized" in str(e):
            return True
        return False
