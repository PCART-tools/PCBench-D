def map_filenames(build_folder: str, fnames: Iterable[str]) -> List[str]:
    return [map_filename(build_folder, fname) for fname in fnames]
