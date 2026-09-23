def embed_headers(
    fname: str, include_dirs: Optional[Union[Sequence[str], Sequence[Path], str]] = None
) -> str:
    if include_dirs is None:
        include_dirs = [Path(__file__).parent.parent.parent]
    elif isinstance(include_dirs, str):
        include_dirs = [Path(include_dirs)]
    else:
        include_dirs = [Path(x) for x in include_dirs]

    return _embed_headers(read_file(fname), include_dirs, {fname})
