def allow_lazy(func, *resultclasses):
    warnings.warn(
        "django.utils.functional.allow_lazy() is deprecated in favor of "
        "django.utils.functional.keep_lazy()",
        RemovedInDjango20Warning, 2)
    return keep_lazy(*resultclasses)(func)
