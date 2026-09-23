def warn_if_tmpdir_flag(args: List[str]) -> None:
    """
    Warn the user that using fast_nvcc with some flags might not work.
    """
    file_path_specs = 'file-and-path-specifications'
    guiding_driver = 'options-for-guiding-compiler-driver'
    scary_flags = {
        '--objdir-as-tempdir': file_path_specs,
        '-objtemp': file_path_specs,
        '--keep': guiding_driver,
        '-keep': guiding_driver,
        '--keep-dir': guiding_driver,
        '-keep-dir': guiding_driver,
        '--save-temps': guiding_driver,
        '-save-temps': guiding_driver,
    }
    for arg in args:
        for flag, frag in scary_flags.items():
            if re.match(fr'^{re.escape(flag)}(?:=.*)?$', arg):
                fast_nvcc_warn(f'{flag} not supported since it interacts with')
                fast_nvcc_warn('TMPDIR, so fast_nvcc may break; see this URL:')
                fast_nvcc_warn(f'{url_base}#{frag}')
