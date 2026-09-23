def _nightly_version(spdir: str) -> str:
    # first get the git version from the installed module
    version_fname = os.path.join(spdir, "torch", "version.py")
    with open(version_fname) as f:
        lines = f.read().splitlines()
    for line in lines:
        if not line.startswith("git_version"):
            continue
        git_version = literal_eval(line.partition("=")[2].strip())
        break
    else:
        raise RuntimeError(f"Could not find git_version in {version_fname}")
    print(f"Found released git version {git_version}")
    # now cross reference with nightly version
    _ensure_commit(git_version)
    cmd = ["git", "show", "--no-patch", "--format=%s", git_version]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, universal_newlines=True)
    m = SHA1_RE.search(p.stdout)
    if m is None:
        raise RuntimeError(
            f"Could not find nightly release in git history:\n  {p.stdout}"
        )
    nightly_version = m.group(1)
    print(f"Found nightly release version {nightly_version}")
    # now checkout nightly version
    _ensure_commit(nightly_version)
    return nightly_version
