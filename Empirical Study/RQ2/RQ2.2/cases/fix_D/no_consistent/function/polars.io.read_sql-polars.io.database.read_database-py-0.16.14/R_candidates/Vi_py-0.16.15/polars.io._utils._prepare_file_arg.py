def _prepare_file_arg(
    file: str | list[str] | TextIO | Path | BinaryIO | bytes,
    encoding: str | None = None,
    use_pyarrow: bool | None = None,
    **kwargs: Any,
) -> ContextManager[str | BinaryIO | list[str] | list[BinaryIO]]:
    """
    Prepare file argument.

    Utility for read_[csv, parquet]. (not to be used by scan_[csv, parquet]).
    Returned value is always usable as a context.

    A :class:`StringIO`, :class:`BytesIO` file is returned as a :class:`BytesIO`.
    A local path is returned as a string.
    An http URL is read into a buffer and returned as a :class:`BytesIO`.

    When ``encoding`` is not ``utf8`` or ``utf8-lossy``, the whole file is
    first read in python and decoded using the specified encoding and
    returned as a :class:`BytesIO` (for usage with ``read_csv``).

    A `bytes` file is returned as a :class:`BytesIO` if ``use_pyarrow=True``.

    When fsspec is installed, remote file(s) is (are) opened with
    `fsspec.open(file, **kwargs)` or `fsspec.open_files(file, **kwargs)`.
    If encoding is not ``utf8`` or ``utf8-lossy``, decoding is handled by
    fsspec too.

    """

    # Small helper to use a variable as context
    @contextmanager
    def managed_file(file: Any) -> Iterator[Any]:
        try:
            yield file
        finally:
            pass

    has_non_utf8_non_utf8_lossy_encoding = (
        encoding not in {"utf8", "utf8-lossy"} if encoding else False
    )
    encoding_str = encoding if encoding else "utf8"

    # PyArrow allows directories, so we only check that something is not
    # a dir if we are not using PyArrow
    check_not_dir = not use_pyarrow

    if isinstance(file, bytes):
        if has_non_utf8_non_utf8_lossy_encoding:
            return _check_empty(
                BytesIO(file.decode(encoding_str).encode("utf8")),
                context="bytes",
            )
        if use_pyarrow:
            return _check_empty(BytesIO(file), context="bytes")

    if isinstance(file, StringIO):
        return _check_empty(
            BytesIO(file.read().encode("utf8")),
            context="StringIO",
            read_position=file.tell(),
        )

    if isinstance(file, BytesIO):
        if has_non_utf8_non_utf8_lossy_encoding:
            return _check_empty(
                BytesIO(file.read().decode(encoding_str).encode("utf8")),
                context="BytesIO",
                read_position=file.tell(),
            )
        return managed_file(
            _check_empty(
                b=file,
                context="BytesIO",
                read_position=file.tell(),
            )
        )

    if isinstance(file, Path):
        if has_non_utf8_non_utf8_lossy_encoding:
            return _check_empty(
                BytesIO(file.read_bytes().decode(encoding_str).encode("utf8")),
                context=f"Path ({file!r})",
            )
        return managed_file(normalise_filepath(file, check_not_dir))

    if isinstance(file, str):
        # make sure that this is before fsspec
        # as fsspec needs requests to be installed
        # to read from http
        if file.startswith("http"):
            return _process_http_file(file, encoding_str)
        if _FSSPEC_AVAILABLE:
            from fsspec.utils import infer_storage_options

            if not has_non_utf8_non_utf8_lossy_encoding:
                if infer_storage_options(file)["protocol"] == "file":
                    return managed_file(normalise_filepath(file, check_not_dir))
            kwargs["encoding"] = encoding
            return fsspec.open(file, **kwargs)

    if isinstance(file, list) and bool(file) and all(isinstance(f, str) for f in file):
        if _FSSPEC_AVAILABLE:
            from fsspec.utils import infer_storage_options

            if not has_non_utf8_non_utf8_lossy_encoding:
                if all(infer_storage_options(f)["protocol"] == "file" for f in file):
                    return managed_file(
                        [normalise_filepath(f, check_not_dir) for f in file]
                    )
            kwargs["encoding"] = encoding
            return fsspec.open_files(file, **kwargs)

    if isinstance(file, str):
        file = normalise_filepath(file, check_not_dir)
        if has_non_utf8_non_utf8_lossy_encoding:
            with open(file, encoding=encoding_str) as f:
                return _check_empty(
                    BytesIO(f.read().encode("utf8")), context=f"{file!r}"
                )

    return managed_file(file)
