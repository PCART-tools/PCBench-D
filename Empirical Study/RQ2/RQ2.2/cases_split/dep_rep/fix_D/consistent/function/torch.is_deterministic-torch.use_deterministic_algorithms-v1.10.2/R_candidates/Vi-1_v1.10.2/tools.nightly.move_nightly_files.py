@timed("Moving nightly files into repo")
def move_nightly_files(spdir: str, platform: str) -> None:
    """Moves PyTorch files from temporary installed location to repo."""
    # get file listing
    source_dir = os.path.join(spdir, "torch")
    target_dir = os.path.abspath("torch")
    listing = _get_listing(source_dir, target_dir, platform)
    # copy / link files
    if platform.startswith("win"):
        _copy_files(listing, source_dir, target_dir)
    else:
        try:
            _link_files(listing, source_dir, target_dir)
        except Exception:
            _copy_files(listing, source_dir, target_dir)
