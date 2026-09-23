def get_post_upload_jobs():
    return [
        {
            "update_s3_htmls": {
                "name": "update_s3_htmls",
                "context": "org-member",
                "filters": branch_filters.gen_filter_dict(
                    branches_list=["postnightly"],
                ),
            },
        },
    ]
