def _get_glibc_version():
    try:
        ver = os.confstr("CS_GNU_LIBC_VERSION").rsplit(" ")[1]
    except Exception:
        ver = "0.0"

    return ver
