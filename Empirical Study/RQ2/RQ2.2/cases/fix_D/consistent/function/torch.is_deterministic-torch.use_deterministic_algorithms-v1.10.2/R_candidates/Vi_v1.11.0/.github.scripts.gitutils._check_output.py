def _check_output(items: List[str], encoding: str = "utf-8") -> str:
    from subprocess import check_output, CalledProcessError
    try:
        return check_output(items).decode(encoding)
    except CalledProcessError as e:
        msg = f"Command `{' '.join(e.cmd)}` returned non-zero exit code {e.returncode}"
        stdout = e.stdout.decode(encoding) if e.stdout is not None else ""
        stderr = e.stderr.decode(encoding) if e.stderr is not None else ""
        if len(stderr) == 0:
            msg += f"\n{stdout}"
        else:
            msg += f"\nstdout:\n{stdout}\nstderr:\n{stderr}"
        raise RuntimeError(msg) from e
