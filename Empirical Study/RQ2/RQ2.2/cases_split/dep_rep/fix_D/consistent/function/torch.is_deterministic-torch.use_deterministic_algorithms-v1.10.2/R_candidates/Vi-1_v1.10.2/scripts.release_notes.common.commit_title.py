def commit_title(commit_hash):
    cmd = f'git log -n 1 --pretty=format:%s {commit_hash}'
    ret, out, err = run(cmd)
    return out if ret == 0 else None
