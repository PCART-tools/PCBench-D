def load_package(
    path: FileLike, model_name: str = "model", run_single_threaded: bool = False
) -> AOTICompiledModel:  # type: ignore[type-arg]
    assert (
        isinstance(path, (io.IOBase, IO)) and path.readable() and path.seekable()
    ) or (isinstance(path, (str, os.PathLike)) and os.fspath(path).endswith(".pt2")), (
        f"Unable to load package. Path must be a buffer or a file ending in .pt2. Instead got {path}"
    )

    if isinstance(path, (io.IOBase, IO)):
        with tempfile.NamedTemporaryFile(suffix=".pt2") as f:
            # TODO(angelayi): We shouldn't need to do this -- miniz should
            # handle reading the buffer. This is just a temporary workaround
            f.write(path.read())
            path.seek(0)
            log.debug("Writing buffer to tmp file located at %s.", f.name)
            loader = torch._C._aoti.AOTIModelPackageLoader(
                f.name, model_name, run_single_threaded
            )  # type: ignore[call-arg]
            return AOTICompiledModel(loader)

    path = os.fspath(path)  # AOTIModelPackageLoader expects (str, str)
    loader = torch._C._aoti.AOTIModelPackageLoader(
        path, model_name, run_single_threaded
    )  # type: ignore[call-arg]
    return AOTICompiledModel(loader)
