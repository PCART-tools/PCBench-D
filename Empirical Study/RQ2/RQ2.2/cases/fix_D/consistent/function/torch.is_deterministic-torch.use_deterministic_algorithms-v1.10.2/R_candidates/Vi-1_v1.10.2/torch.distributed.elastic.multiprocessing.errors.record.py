def record(
    fn: Callable[..., T], error_handler: Optional[ErrorHandler] = None
) -> Callable[..., T]:
    """
    Syntactic sugar to record errors/exceptions that happened in the decorated
    function using the provided ``error_handler``.

    Using this decorator is equivalent to:

    ::

     error_handler = get_error_handler()
     error_handler.initialize()
     try:
        foobar()
     except ChildFailedError as e:
        _, failure = e.get_first_failure()
        error_handler.dump_error_file(failure.error_file, failure.exitcode)
        raise
     except Exception as e:
        error_handler.record(e)
        raise

    .. important:: use this decorator once per process at the top level method,
                   typically this is the main method.

    Example

    ::

     @record
     def main():
         pass

     if __name__=="__main__":
        main()

    """

    if not error_handler:
        error_handler = get_error_handler()

    def wrap(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            assert error_handler is not None  # assertion for mypy type checker
            error_handler.initialize()
            try:
                return f(*args, **kwargs)
            except ChildFailedError as e:
                rank, failure = e.get_first_failure()
                if failure.error_file != _NOT_AVAILABLE:
                    error_handler.dump_error_file(failure.error_file, failure.exitcode)
                else:
                    log.info(
                        (
                            f"local_rank {rank} FAILED with no error file."
                            f" Decorate your entrypoint fn with @record for traceback info."
                            f" See: https://pytorch.org/docs/stable/elastic/errors.html"
                        )
                    )
                raise
            except Exception as e:
                error_handler.record_exception(e)
                raise

        return wrapper

    return wrap(fn)
