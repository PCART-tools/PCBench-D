def setup_gha_env(name: str, val: str) -> None:
    fname = os.environ["GITHUB_ENV"]
    content = f"{name}={val}\n"
    with open(fname, "a") as fo:
        fo.write(content)
