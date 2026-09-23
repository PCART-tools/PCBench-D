def _parse_repo_info(github):
    if ':' in github:
        repo_info, branch = github.split(':')
    else:
        repo_info, branch = github, None
    repo_owner, repo_name = repo_info.split('/')

    if branch is None:
        # The branch wasn't specified by the user, so we need to figure out the
        # default branch: main or master. Our assumption is that if main exists
        # then it's the default branch, otherwise it's master.
        try:
            with urlopen(f"https://github.com/{repo_owner}/{repo_name}/tree/main/"):
                branch = 'main'
        except HTTPError as e:
            if e.code == 404:
                branch = 'master'
            else:
                raise
    return repo_owner, repo_name, branch
