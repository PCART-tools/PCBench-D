def find_matching_merge_rule(pr: GitHubPR, repo: GitRepo) -> MergeRule:
    """Returns merge rule matching to this pr or raises an exception"""
    changed_files = pr.get_changed_files()
    approved_by = set(pr.get_approved_by())
    rules = read_merge_rules(repo)
    for rule in rules:
        rule_name = rule.name
        rule_approvers_set = set(rule.approved_by)
        patterns_re = patterns_to_regex(rule.patterns)
        approvers_intersection = approved_by.intersection(rule_approvers_set)
        # If rule requires approvers but they aren't the ones that reviewed PR
        if len(approvers_intersection) == 0 and len(rule_approvers_set) > 0:
            print(f"Skipping rule {rule_name} due to no approvers overlap")
            continue
        if rule.mandatory_app_id is not None:
            cs_conslusions = pr.get_check_suite_conclusions()
            mandatory_app_id = rule.mandatory_app_id
            if mandatory_app_id not in cs_conslusions or cs_conslusions[mandatory_app_id] != "SUCCESS":
                print(f"Skipping rule {rule_name} as mandatory app {mandatory_app_id} is not in {cs_conslusions}")
                continue
        non_matching_files = []
        for fname in changed_files:
            if not patterns_re.match(fname):
                non_matching_files.append(fname)
        if len(non_matching_files) > 0:
            print(f"Skipping rule {rule_name} due to non-matching files: {non_matching_files}")
            continue
        print(f"Matched rule {rule_name} for {pr.pr_num}")
        return rule
    raise RuntimeError(f"PR {pr.pr_num} does not match merge rules")
