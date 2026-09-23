def _parse_reveals(file: IO[str]) -> List[str]:
    """Extract and parse all ``"  # E: "`` comments from the passed file-like object.

    All format keys will be substituted for their respective value from `FORMAT_DICT`,
    *e.g.* ``"{Tensor}"`` becomes ``"torch.tensor.Tensor"``.
    """
    string = file.read().replace("*", "")

    # Grab all `# E:`-based comments
    comments_array = list(map(lambda str: str.partition("  # E: ")[2], string.split("\n")))
    comments = "/n".join(comments_array)

    # Only search for the `{*}` pattern within comments,
    # otherwise there is the risk of accidently grabbing dictionaries and sets
    key_set = set(re.findall(r"\{(.*?)\}", comments))
    kwargs = {
        k: FORMAT_DICT.get(k, f"<UNRECOGNIZED FORMAT KEY {k!r}>") for k in key_set
    }
    fmt_str = comments.format(**kwargs)

    return fmt_str.split("/n")
