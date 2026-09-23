def _get_build_directory(name: str, verbose: bool) -> str:
    root_extensions_directory = os.environ.get('TORCH_EXTENSIONS_DIR')
    if root_extensions_directory is None:
        root_extensions_directory = get_default_build_root()
        cu_str = ('cpu' if torch.version.cuda is None else
                  f'cu{torch.version.cuda.replace(".", "")}')  # type: ignore[attr-defined]
        python_version = f'py{sys.version_info.major}{sys.version_info.minor}'
        build_folder = f'{python_version}_{cu_str}'

        root_extensions_directory = os.path.join(
            root_extensions_directory, build_folder)

    if verbose:
        print(f'Using {root_extensions_directory} as PyTorch extensions root...')

    build_directory = os.path.join(root_extensions_directory, name)
    if not os.path.exists(build_directory):
        if verbose:
            print(f'Creating extension directory {build_directory}...')
        # This is like mkdir -p, i.e. will also create parent directories.
        os.makedirs(build_directory, exist_ok=True)

    return build_directory
