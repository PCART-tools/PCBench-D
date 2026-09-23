def profile(group=None):
    """
    @profile decorator adds latency and success/failure metrics to any given function.

    Usage

    ::

     @metrics.profile("my_metric_group")
     def some_function(<arguments>):
    """
    warnings.warn("Deprecated, use @prof instead", DeprecationWarning)

    def wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                publish_metric(group, "{}.success".format(func.__name__), 1)
            except Exception:
                publish_metric(group, "{}.failure".format(func.__name__), 1)
                raise
            finally:
                publish_metric(
                    group,
                    "{}.duration.ms".format(func.__name__),
                    get_elapsed_time_ms(start_time),
                )
            return result

        return wrapper

    return wrap
