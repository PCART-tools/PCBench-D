def _worker_compile_cpp(
    lock_path: str,
    cpp_builder: CppBuilder,
) -> None:
    from torch.utils._filelock import FileLock

    with FileLock(lock_path, timeout=LOCK_TIMEOUT):
        if not os.path.exists(cpp_builder.get_target_file_path()):
            cpp_builder.build()
