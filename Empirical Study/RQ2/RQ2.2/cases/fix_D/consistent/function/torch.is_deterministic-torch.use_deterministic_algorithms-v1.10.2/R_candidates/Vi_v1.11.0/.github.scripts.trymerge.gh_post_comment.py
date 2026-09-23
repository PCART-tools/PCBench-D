def gh_post_comment(org: str, project: str, pr_num: int, comment: str, dry_run: bool = False) -> List[Dict[str, Any]]:
    if dry_run:
        print(comment)
        return []
    return fetch_json(f'https://api.github.com/repos/{org}/{project}/issues/{pr_num}/comments',
                      data={"body": comment})
