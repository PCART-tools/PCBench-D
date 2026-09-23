def scoped_load_inline(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        def load_inline(*args, **kwargs):
            if IS_WINDOWS:
                # TODO(xmfan): even using TemporaryDirectoryName will result in permission error
                return cpp_extension.load_inline(*args, **kwargs)

            assert "build_directory" not in kwargs
            with TemporaryDirectoryName() as temp_dir_name:
                if kwargs.get("verbose", False):
                    print(f'Using temporary extension directory {temp_dir_name}...', file=sys.stderr)
                kwargs["build_directory"] = temp_dir_name
                return cpp_extension.load_inline(*args, **kwargs)

        return func(*args, load_inline=load_inline, **kwargs)

    return wrapper
