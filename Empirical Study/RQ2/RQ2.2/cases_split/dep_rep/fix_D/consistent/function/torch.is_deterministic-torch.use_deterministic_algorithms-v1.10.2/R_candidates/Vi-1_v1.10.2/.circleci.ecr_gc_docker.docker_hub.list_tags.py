def list_tags(repo, token):
    r = requests.get(
        "https://hub.docker.com/v2/repositories/" + repo + "/tags", headers=token
    )
    r.raise_for_status()
    return [
        IMAGE_INFO(
            repo=repo,
            tag=t["name"],
            size=t["full_size"],
            last_updated_at=t["last_updated"],
            last_updated_by=t["last_updater_username"],
        )
        for t in r.json().get("results", [])
    ]
