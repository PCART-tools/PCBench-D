def try_revert(repo: GitRepo, pr: GitHubPR, dry_run: bool = False) -> None:
    def post_comment(msg: str) -> None:
        gh_post_comment(pr.org, pr.project, pr.pr_num, msg, dry_run=dry_run)
    if not pr.is_closed():
        return post_comment(f"Can't revert open PR #{pr.pr_num}")
    if not RE_REVERT_CMD.match(pr.get_comment_body()):
        raise RuntimeError(f"Comment {pr.get_comment_body()} does not seem to be a valid revert command")
    if pr.get_comment_editor_login() is not None:
        return post_comment("Don't want to revert based on edited command")
    author_association = pr.get_comment_author_association()
    author_login = pr.get_comment_author_login()
    # For some reason, one can not be a member of private repo, only CONTRIBUTOR
    expected_association = "CONTRIBUTOR" if pr.is_base_repo_private() else "MEMBER"
    if author_association != expected_association and author_association != "OWNER":
        return post_comment(f"Will not revert as @{author_login} is not a {expected_association}, but {author_association}")

    # Raises exception if matching rule is not found
    find_matching_merge_rule(pr, repo)
    commit_sha = pr.get_merge_commit()
    if commit_sha is None:
        commits = repo.commits_resolving_gh_pr(pr.pr_num)
        if len(commits) == 0:
            raise RuntimeError("Can't find any commits resolving PR")
        commit_sha = commits[0]
    msg = repo.commit_message(commit_sha)
    rc = RE_DIFF_REV.search(msg)
    if rc is not None:
        raise RuntimeError(f"Can't revert PR that was landed via phabricator as {rc.group(1)}")
    repo.checkout(pr.default_branch())
    repo.revert(commit_sha)
    msg = repo.commit_message("HEAD")
    msg = re.sub(RE_PULL_REQUEST_RESOLVED, "", msg)
    msg += f"\nReverted {pr.get_pr_url()} on behalf of @{author_login}\n"
    repo.amend_commit_message(msg)
    repo.push(pr.default_branch(), dry_run)
    if not dry_run:
        gh_add_labels(pr.org, pr.project, pr.pr_num, ["reverted"])
