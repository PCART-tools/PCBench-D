def main() -> None:
    args = parse_args()
    repo = GitRepo(get_git_repo_dir(), get_git_remote_name())
    org, project = repo.gh_owner_and_name()

    pr = GitHubPR(org, project, args.pr_num)
    if args.revert:
        try:
            try_revert(repo, pr, dry_run=args.dry_run)
        except Exception as e:
            msg = f"Reverting PR {args.pr_num} failed due to {e}"
            run_url = os.getenv("GH_RUN_URL")
            if run_url is not None:
                msg += f"\nRaised by {run_url}"
            gh_post_comment(org, project, args.pr_num, msg, dry_run=args.dry_run)
        return

    if pr.is_closed():
        gh_post_comment(org, project, args.pr_num, f"Can't merge closed PR #{args.pr_num}", dry_run=args.dry_run)
        return

    if pr.is_cross_repo():
        gh_post_comment(org, project, args.pr_num, "Cross-repo merges are not supported at the moment", dry_run=args.dry_run)
        return

    try:
        pr.merge_into(repo, dry_run=args.dry_run)
    except Exception as e:
        msg = f"Merge failed due to {e}"
        run_url = os.getenv("GH_RUN_URL")
        if run_url is not None:
            msg += f"\nRaised by {run_url}"
        gh_post_comment(org, project, args.pr_num, msg, dry_run=args.dry_run)
