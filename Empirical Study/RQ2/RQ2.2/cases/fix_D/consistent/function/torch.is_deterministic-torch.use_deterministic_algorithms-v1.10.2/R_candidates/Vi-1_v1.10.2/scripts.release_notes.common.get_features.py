def get_features(commit_hash, return_dict=False):
    title, body, files_changed = (
        commit_title(commit_hash),
        commit_body(commit_hash),
        commit_files_changed(commit_hash))
    pr_number = parse_pr_number(body, commit_hash, title)
    labels = []
    if pr_number is not None:
        labels = gh_labels(pr_number)
    result = Features(title, body, pr_number, files_changed, labels)
    if return_dict:
        return features_to_dict(result)
    return result
