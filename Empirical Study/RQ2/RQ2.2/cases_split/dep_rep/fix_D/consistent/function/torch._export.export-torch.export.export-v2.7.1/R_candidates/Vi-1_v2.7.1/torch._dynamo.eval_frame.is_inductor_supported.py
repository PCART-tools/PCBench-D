def is_inductor_supported():
    try:
        check_if_inductor_supported()
        return True
    except Exception:
        return False
