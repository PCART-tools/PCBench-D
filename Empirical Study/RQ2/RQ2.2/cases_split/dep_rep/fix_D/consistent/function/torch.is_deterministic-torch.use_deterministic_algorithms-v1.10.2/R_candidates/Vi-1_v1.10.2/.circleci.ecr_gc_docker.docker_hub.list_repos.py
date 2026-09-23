def list_repos(user, token):
    r = requests.get("https://hub.docker.com/v2/repositories/" + user, headers=token)
    r.raise_for_status()
    ret = sorted(
        repo["user"] + "/" + repo["name"] for repo in r.json().get("results", [])
    )
    if ret:
        print("repos found:")
        print("".join("\n\t" + r for r in ret))
    return ret
