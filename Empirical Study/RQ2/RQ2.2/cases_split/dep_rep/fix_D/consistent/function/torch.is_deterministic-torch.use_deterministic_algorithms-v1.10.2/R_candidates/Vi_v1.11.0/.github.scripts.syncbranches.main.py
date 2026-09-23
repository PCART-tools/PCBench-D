def main() -> None:
    args = parse_args()
    repo = GitRepo(get_git_repo_dir(), debug=args.debug)
    repo.cherry_pick_commits(args.sync_branch, args.default_branch)
    repo.push(args.default_branch, args.dry_run)
