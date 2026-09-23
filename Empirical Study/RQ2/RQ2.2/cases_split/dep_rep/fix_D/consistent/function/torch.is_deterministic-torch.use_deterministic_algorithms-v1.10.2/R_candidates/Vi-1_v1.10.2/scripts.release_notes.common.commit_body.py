def commit_body(commit_hash):
    cmd = f'git log -n 1 --pretty=format:%b {commit_hash}'
    ret, out, err = run(cmd)
    return out if ret == 0 else None
