def check_file(filename, is_inlined_call=False):
    """Should skip this file?"""
    if filename is None:
        return SkipResult(True, "filename is None")
    filename = _as_posix_path(filename)
    if filename in FORCE_SKIP_FILES:
        return SkipResult(True, "FORCE_SKIP_FILES")

    if any(filename.startswith(d) for d in get_legacy_mod_inlinelist()):
        return SkipResult(
            False,
            "LEGACY_MOD_INLINELIST",
        )
    if is_inlined_call and is_torch_inline_allowed(filename):
        return SkipResult(
            False,
            "MOD_INLINELIST",
        )
    if (
        is_fbcode
        and FBCODE_SKIP_DIRS
        and bool(FBCODE_SKIP_DIRS_RE.match(filename))
        and not bool(FBCODE_INLINE_FILES_IN_SKIPPED_DIRS_RE.match(filename))
    ):
        return SkipResult(
            True,
            "FBCODE_SKIP_DIRS",
        )

    if (
        is_fbcode
        and torch._dynamo.config.skip_torchrec
        and FBCODE_SKIP_TORCHREC_DIRS
        and bool(FBCODE_SKIP_TORCHREC_DIRS_RE.match(filename))
        and not bool(FBCODE_INLINE_FILES_IN_SKIPPED_DIRS_RE.match(filename))
    ):
        return SkipResult(True, "FBCODE_SKIP_TORCHREC_DIRS")

    if bool(SKIP_DIRS_RE.match(filename)):
        return SkipResult(True, "SKIP_DIRS")

    if any(filename.startswith(d) for d in get_mod_skiplist()):
        return SkipResult(True, "MOD_SKIPLIST")
    return SkipResult(False, "inlined by default")
