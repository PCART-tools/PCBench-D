def save(
    ep: ExportedProgram,
    f: FileLike,
    *,
    extra_files: Optional[dict[str, Any]] = None,
    opset_version: Optional[dict[str, int]] = None,
    pickle_protocol: int = DEFAULT_PICKLE_PROTOCOL,
) -> None:
    """

    .. warning::
        Under active development, saved files may not be usable in newer versions
        of PyTorch.

    Saves an :class:`ExportedProgram` to a file-like object. It can then be
    loaded using the Python API :func:`torch.export.load <torch.export.load>`.

    Args:
        ep (ExportedProgram): The exported program to save.

        f (str | os.PathLike[str] | IO[bytes]) A file-like object (has to
         implement write and flush) or a string containing a file name.

        extra_files (Optional[Dict[str, Any]]): Map from filename to contents
         which will be stored as part of f.

        opset_version (Optional[Dict[str, int]]): A map of opset names
         to the version of this opset

        pickle_protocol: can be specified to override the default protocol

    Example::

        import torch
        import io


        class MyModule(torch.nn.Module):
            def forward(self, x):
                return x + 10


        ep = torch.export.export(MyModule(), (torch.randn(5),))

        # Save to file
        torch.export.save(ep, "exported_program.pt2")

        # Save to io.BytesIO buffer
        buffer = io.BytesIO()
        torch.export.save(ep, buffer)

        # Save with extra files
        extra_files = {"foo.txt": b"bar".decode("utf-8")}
        torch.export.save(ep, "exported_program.pt2", extra_files=extra_files)

    """
    if not isinstance(ep, ExportedProgram):
        raise TypeError(
            f"The 'ep' parameter must be an instance of 'ExportedProgram', got '{type(ep).__name__}' instead."
        )

    from torch.export.pt2_archive._package import package_pt2

    package_pt2(
        f,
        exported_programs={"model": ep},
        extra_files=extra_files,
        pickle_protocol=pickle_protocol,
        opset_version=opset_version,
    )
