def with_nccl_blocking_wait(func):
    """
    Convenience decorator to set/unset NCCL_BLOCKING_WAIT flag. Note that use of
    this decorator will override the setting of NCCL_ASYNC_ERROR_HANDLING for
    the particular test. After the test, both NCCL_BLOCKING_WAIT and
    NCCL_ASYNC_ERROR_HANDLING will be restored to their original values.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Save and unset NCCL_ASYNC_ERROR_HANDLING
        try:
            cached_nccl_async_error_handling: Union[str, None] = os.environ[
                "NCCL_ASYNC_ERROR_HANDLING"
            ]
            del os.environ["NCCL_ASYNC_ERROR_HANDLING"]
        except KeyError:
            # NCCL_ASYNC_ERROR_HANDLING was unset
            cached_nccl_async_error_handling = None

        # Save val of NCCL_BLOCKING_WAIT and set it.
        try:
            cached_nccl_blocking_wait: Union[str, None] = os.environ[
                "NCCL_BLOCKING_WAIT"
            ]
        except KeyError:
            cached_nccl_blocking_wait = None
        finally:
            os.environ["NCCL_BLOCKING_WAIT"] = "1"

        try:
            ret = func(*args, **kwargs)
            return ret
        finally:
            # restore old values.
            if cached_nccl_async_error_handling is not None:
                os.environ[
                    "NCCL_ASYNC_ERROR_HANDLING"
                ] = cached_nccl_async_error_handling

            if cached_nccl_blocking_wait is not None:
                os.environ["NCCL_BLOCKING_WAIT"] = cached_nccl_blocking_wait

    return wrapper
