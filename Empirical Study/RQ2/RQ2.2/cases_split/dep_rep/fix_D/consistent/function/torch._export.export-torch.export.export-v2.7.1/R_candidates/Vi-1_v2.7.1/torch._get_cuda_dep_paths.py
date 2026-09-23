def _get_cuda_dep_paths(path: str, lib_folder: str, lib_name: str) -> list[str]:
    # Libraries can either be in path/nvidia/lib_folder/lib or path/lib_folder/lib
    nvidia_lib_paths = glob.glob(
        os.path.join(path, "nvidia", lib_folder, "lib", lib_name)
    )
    lib_paths = glob.glob(os.path.join(path, lib_folder, "lib", lib_name))

    return nvidia_lib_paths + lib_paths
