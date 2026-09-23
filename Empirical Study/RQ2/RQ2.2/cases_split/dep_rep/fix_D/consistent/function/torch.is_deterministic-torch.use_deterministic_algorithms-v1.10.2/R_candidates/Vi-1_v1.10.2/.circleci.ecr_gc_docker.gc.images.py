def images(client, repository):
    paginator = client.get_paginator("describe_images")
    pages = paginator.paginate(
        registryId="308535385114", repositoryName=repository["repositoryName"]
    )
    for page in pages:
        for image in page["imageDetails"]:
            yield image
