def gen_workflow_job(channel: str):
    return OrderedDict(
        {
            "anaconda_prune": OrderedDict(
                {
                    "name": f"anaconda-prune-{channel}",
                    "context": quote("org-member"),
                    "packages": quote(PACKAGES_TO_PRUNE),
                    "channel": channel,
                    "filters": gen_filter_dict(branches_list=["postnightly"]),
                }
            )
        }
    )
