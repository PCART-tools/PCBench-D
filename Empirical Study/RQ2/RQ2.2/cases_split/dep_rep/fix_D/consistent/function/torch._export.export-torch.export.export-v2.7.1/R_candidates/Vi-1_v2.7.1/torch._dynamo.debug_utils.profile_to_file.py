def profile_to_file(filename: str) -> Callable[[T], T]:
    """
    Decorator to cProfile a given function and save the result to disk on process exit.

    Args:
        filename: filename to save profile to
    """
    prof = cProfile.Profile()
    filename = os.path.abspath(os.path.expanduser(filename))

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            prof.enable()
            try:
                return fn(*args, **kwargs)
            finally:
                prof.disable()

        return wrapper

    def save_it():
        prof.dump_stats(filename)
        sys.stderr.write(
            textwrap.dedent(
                f"""\
                Wrote profile to {filename}, view with:

                    snakeviz {filename}

                """
            )
        )

    atexit.register(save_it)
    return decorator
