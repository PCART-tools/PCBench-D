def _get_listing_win(source_dir: str) -> List[str]:
    listing = glob.glob(os.path.join(source_dir, "*.pyd"))
    listing.extend(glob.glob(os.path.join(source_dir, "lib", "*.lib")))
    listing.extend(glob.glob(os.path.join(source_dir, "lib", "*.dll")))
    return listing
