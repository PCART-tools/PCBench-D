def main(args: List[str]) -> None:
    """
    Run mypy on one Python file using the correct config file(s).

    This function assumes the following preconditions hold:

    - the cwd is set to the root of this cloned repo
    - args is a valid list of CLI arguments that could be passed to mypy
    - some of args are absolute paths to files to typecheck
    - all the other args are config flags for mypy, rather than files

    These assumptions hold, for instance, when mypy is run automatically
    by VS Code's Python extension, so in your clone of this repository,
    you could modify your .vscode/settings.json to look something like
    this (assuming you use a conda environment named "pytorch"):

        {
          "python.linting.enabled": true,
          "python.linting.mypyEnabled": true,
          "python.linting.mypyPath":
            "${env:HOME}/miniconda3/envs/pytorch/bin/python",
          "python.linting.mypyArgs": [
            "${workspaceFolder}/tools/linter/mypy_wrapper.py"
          ]
        }

    More generally, this should work for any editor sets the cwd to the
    repo root, runs mypy on individual files via their absolute paths,
    and allows you to set the path to the mypy executable.
    """
    repo_root = str(Path.cwd())
    exit_code, mypy_issues, stderrs = run(
        args=[arg for arg in args if not arg.startswith(repo_root)],
        files=[arg for arg in args if arg.startswith(repo_root)],
    )
    for issue in mypy_issues:
        print(issue)
    for stderr in stderrs:
        print(stderr, end='', file=sys.stderr)
    sys.exit(exit_code)
