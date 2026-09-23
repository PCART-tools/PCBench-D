def lib_paths_from_base(base_path: str) -> List[str]:
    return [os.path.join(base_path, s) for s in ['lib/x64', 'lib', 'lib64']]
