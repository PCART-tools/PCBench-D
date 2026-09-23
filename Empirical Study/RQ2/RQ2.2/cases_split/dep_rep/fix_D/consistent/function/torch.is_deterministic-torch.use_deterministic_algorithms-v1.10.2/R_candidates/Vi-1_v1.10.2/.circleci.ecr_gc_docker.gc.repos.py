def repos(client):
    paginator = client.get_paginator("describe_repositories")
    pages = paginator.paginate(registryId="308535385114")
    for page in pages:
        for repo in page["repositories"]:
            yield repo
