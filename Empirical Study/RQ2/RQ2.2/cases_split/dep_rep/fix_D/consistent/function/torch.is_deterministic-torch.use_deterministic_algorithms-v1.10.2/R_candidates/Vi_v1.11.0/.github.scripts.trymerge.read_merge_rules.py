def read_merge_rules(repo: GitRepo) -> List[MergeRule]:
    from pathlib import Path
    rules_path = Path(repo.repo_dir) / ".github" / "merge_rules.json"
    if not rules_path.exists():
        print(f"{rules_path} does not exist, returning empty rules")
        return []
    with open(rules_path) as fp:
        rc = json.load(fp, object_hook=lambda x: MergeRule(**x))
    return cast(List[MergeRule], rc)
