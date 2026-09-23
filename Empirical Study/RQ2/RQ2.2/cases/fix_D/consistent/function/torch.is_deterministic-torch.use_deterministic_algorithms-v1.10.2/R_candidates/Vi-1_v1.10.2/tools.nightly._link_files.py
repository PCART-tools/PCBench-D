def _link_files(listing: List[str], source_dir: str, target_dir: str) -> None:
    for src in listing:
        _move_single(src, source_dir, target_dir, os.link, "Linking")
