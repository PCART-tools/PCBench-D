def _get_listing_osx(source_dir: str) -> List[str]:
    # oddly, these are .so files even on Mac
    listing = glob.glob(os.path.join(source_dir, "*.so"))
    listing.extend(glob.glob(os.path.join(source_dir, "lib", "*.dylib")))
    return listing
