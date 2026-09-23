def getURLFromName(name, filename):
    return "{base_url}{name}/{filename}".format(base_url=DOWNLOAD_BASE_URL,
                                                name=name, filename=filename)
