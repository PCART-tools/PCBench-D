def check_lambda_fn(fn):
    # Partial object has no attribute '__name__', but can be pickled
    if hasattr(fn, "__name__") and fn.__name__ == "<lambda>" and not DILL_AVAILABLE:
        warnings.warn(
            "Lambda function is not supported for pickle, please use "
            "regular python function or functools.partial instead."
        )
