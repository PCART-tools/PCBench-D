def skip_if_win32():
    return sandcastle_skip_if(
        sys.platform == 'win32',
        "This unit test case is not supportted on Windows platform",
    )
