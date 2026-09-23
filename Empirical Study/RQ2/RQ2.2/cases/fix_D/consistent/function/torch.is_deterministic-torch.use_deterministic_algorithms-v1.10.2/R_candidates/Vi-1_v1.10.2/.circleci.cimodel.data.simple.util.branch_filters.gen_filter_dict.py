def gen_filter_dict(
        branches_list=NON_PR_BRANCH_LIST,
        tags_list=None
):
    """Generates a filter dictionary for use with CircleCI's job filter"""
    filter_dict = {
        "branches": {
            "only": branches_list,
        },
    }

    if tags_list is not None:
        filter_dict["tags"] = {"only": tags_list}
    return filter_dict
