@deprecated("Deprecated, use `@prof` instead", category=FutureWarning)
def profile(group=None):
    """
    @profile decorator adds latency and success/failure metrics to any given function.

    Usage

    ::

     @metrics.profile("my_metric_group")
     def some_function(<arguments>):
    """

    def wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                publish_metric(group, f"{func.__name__}.success", 1)
            except Exception:
                publish_metric(group, f"{func.__name__}.failure", 1)
                raise
            finally:
                publish_metric(
                    group,
                    f"{func.__name__}.duration.ms",
                    get_elapsed_time_ms(start_time),  # type: ignore[possibly-undefined]
                )
            return result

        return wrapper

    return wrap
