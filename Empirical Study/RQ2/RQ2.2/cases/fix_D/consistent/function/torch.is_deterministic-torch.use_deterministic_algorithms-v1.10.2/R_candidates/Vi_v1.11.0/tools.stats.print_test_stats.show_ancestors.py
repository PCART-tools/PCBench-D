def show_ancestors(num_commits: int) -> str:
    return f'    | : ({num_commits} commit{plural(num_commits)})'
