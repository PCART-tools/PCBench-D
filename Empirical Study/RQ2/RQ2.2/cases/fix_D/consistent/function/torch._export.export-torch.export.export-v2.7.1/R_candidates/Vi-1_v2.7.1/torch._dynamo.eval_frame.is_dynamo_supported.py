def is_dynamo_supported():
    try:
        check_if_dynamo_supported()
        return True
    except Exception:
        return False
