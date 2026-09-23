def get_correct_mypy_version():
    # there's probably a more elegant way to do this
    match, = re.finditer(
        r'mypy==(\d+(?:\.\d+)*)',
        Path('.circleci/docker/common/install_conda.sh').read_text(),
    )
    version, = match.groups()
    return version
