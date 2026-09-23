@functools.lru_cache(None)
def try_import_cutlass() -> bool:
    """
    We want to support three ways of passing in CUTLASS:
    1. fbcode, handled by the internal build system.
    2. pip install nvidia-cutlass, which provides the cutlass_library package
       and the header files in the cutlass_library/source directory.
    3. User specifies cutlass_dir. The default is ../third_party/cutlass/,
       which is the directory when developers build from source.
    """
    if config.is_fbcode():
        return True

    try:
        import cutlass  # type: ignore[import-not-found]
        import cutlass_library  # type: ignore[import-not-found]

        cutlass_minor_vesion = int(cutlass.__version__.split(".")[1])
        if cutlass_minor_vesion < 7:
            log.warning("CUTLASS version < 3.7 is not recommended.")

        log.debug(
            "Found cutlass_library in python search path, overriding config.cuda.cutlass_dir"
        )
        cutlass_library_dir = os.path.dirname(cutlass_library.__file__)
        assert os.path.isdir(cutlass_library_dir), (
            f"{cutlass_library_dir} is not a directory"
        )
        config.cuda.cutlass_dir = os.path.abspath(
            os.path.join(
                cutlass_library_dir,
                "source",
            )
        )
        return True
    except ModuleNotFoundError:
        log.debug(
            "cutlass_library not found in sys.path, trying to import from config.cuda.cutlass_dir"
        )

    # Copy CUTLASS python scripts to a temp dir and add the temp dir to Python search path.
    # This is a temporary hack to avoid CUTLASS module naming conflicts.
    # TODO(ipiszy): remove this hack when CUTLASS solves Python scripts packaging structure issues.

    cutlass_py_full_path = os.path.abspath(
        os.path.join(config.cuda.cutlass_dir, "python/cutlass_library")
    )
    tmp_cutlass_py_full_path = os.path.abspath(
        os.path.join(cache_dir(), "torch_cutlass_library")
    )
    dst_link = os.path.join(tmp_cutlass_py_full_path, "cutlass_library")

    if os.path.isdir(cutlass_py_full_path):
        if tmp_cutlass_py_full_path not in sys.path:
            if os.path.exists(dst_link):
                assert os.path.islink(dst_link), (
                    f"{dst_link} is not a symlink. Try to remove {dst_link} manually and try again."
                )
                assert os.path.realpath(os.readlink(dst_link)) == os.path.realpath(
                    cutlass_py_full_path
                ), f"Symlink at {dst_link} does not point to {cutlass_py_full_path}"
            else:
                os.makedirs(tmp_cutlass_py_full_path, exist_ok=True)
                os.symlink(cutlass_py_full_path, dst_link)
            sys.path.append(tmp_cutlass_py_full_path)
        try:
            import cutlass_library.generator  # noqa: F401
            import cutlass_library.library  # noqa: F401
            import cutlass_library.manifest  # noqa: F401

            return True
        except ImportError as e:
            log.debug(
                "Failed to import CUTLASS packages: %s, ignoring the CUTLASS backend.",
                str(e),
            )
    else:
        log.debug(
            "Failed to import CUTLASS packages: CUTLASS repo does not exist: %s",
            cutlass_py_full_path,
        )
    return False
