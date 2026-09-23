def aoti_load_package(path: FileLike, run_single_threaded: bool = False) -> Any:  # type: ignore[type-arg]
    """
    Loads the model from the PT2 package.

    If multiple models were packaged into the PT2, this will load the default
    model. To load a specific model, you can directly call the load API

    .. code-block:: python

        from torch._inductor.package import load_package

        compiled_model1 = load_package("my_package.pt2", "model1")
        compiled_model2 = load_package("my_package.pt2", "model2")

    Args:
        path: Path to the .pt2 package
        run_single_threaded (bool): Whether the model should be run without
            thread synchronization logic. This is useful to avoid conflicts with
            CUDAGraphs.
    """
    from torch._inductor.package import load_package

    return load_package(path, run_single_threaded=run_single_threaded)
