def get_tag() -> str:
    root = get_pytorch_root()
    # We're on a tag
    am_on_tag = (
        subprocess.run(
            ['git', 'describe', '--tags', '--exact'],
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ).returncode == 0
    )
    tag = ""
    if am_on_tag:
        dirty_tag = subprocess.check_output(
            ['git', 'describe'],
            cwd=root
        ).decode('ascii').strip()
        # Strip leading v that we typically do when we tag branches
        # ie: v1.7.1 -> 1.7.1
        tag = re.sub(LEADING_V_PATTERN, "", dirty_tag)
        # Strip trailing rc pattern
        # ie: 1.7.1-rc1 -> 1.7.1
        tag = re.sub(TRAILING_RC_PATTERN, "", tag)
    return tag
