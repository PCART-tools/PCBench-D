def _get_listing(source_dir: str, target_dir: str, platform: str) -> List[str]:
    if platform.startswith("linux"):
        listing = _get_listing_linux(source_dir)
    elif platform.startswith("osx"):
        listing = _get_listing_osx(source_dir)
    elif platform.startswith("win"):
        listing = _get_listing_win(source_dir)
    else:
        raise RuntimeError(f"Platform {platform!r} not recognized")
    listing.extend(_find_missing_pyi(source_dir, target_dir))
    listing.append(os.path.join(source_dir, "version.py"))
    listing.append(os.path.join(source_dir, "testing", "_internal", "generated"))
    listing.append(os.path.join(source_dir, "bin"))
    listing.append(os.path.join(source_dir, "include"))
    return listing
