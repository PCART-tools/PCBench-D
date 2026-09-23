def import_transformers_or_skip():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                from transformers import (  # noqa: F401
                    AutoModelForMaskedLM,
                    BertConfig,
                )

                return func(*args, **kwargs)
            except ImportError:
                sys.exit(TEST_SKIPS["importerror"].exit_code)

        return wrapper

    return decorator
