@functools.lru_cache(None)
def has_safetensors_and_transformers():
    try:
        # safetensors is not an exporter requirement, but needed for some huggingface models
        import safetensors  # type: ignore[import]  # noqa: F401
        import transformers  # type: ignore[import]  # noqa: F401
        from safetensors import torch as safetensors_torch  # noqa: F401

        return True
    except ImportError:
        return False
