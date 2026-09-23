def _process_http_file(path: str, encoding: str | None = None) -> BytesIO:
    from urllib.request import urlopen

    with urlopen(path) as f:
        if not encoding or encoding in {"utf8", "utf8-lossy"}:
            return BytesIO(f.read())
        else:
            return BytesIO(f.read().decode(encoding).encode("utf8"))
