def _get_listing_linux(source_dir: str) -> List[str]:
    listing = glob.glob(os.path.join(source_dir, "*.so"))
    listing.extend(glob.glob(os.path.join(source_dir, "lib", "*.so")))
    return listing
