def downloadFromURLToFile(url, filename, show_progress=True):
    try:
        print("Downloading from {url}".format(url=url))
        response = urllib.urlopen(url)
        size = int(response.info().get('Content-Length').strip())
        chunk = min(size, 8192)
        print("Writing to {filename}".format(filename=filename))
        if show_progress:
            downloaded_size = 0
            progressBar(0)
        with open(filename, "wb") as local_file:
            while True:
                data_chunk = response.read(chunk)
                if not data_chunk:
                    break
                local_file.write(data_chunk)
                if show_progress:
                    downloaded_size += len(data_chunk)
                    progressBar(int(100 * downloaded_size / size))
        print("")  # New line to fix for progress bar
    except HTTPError as e:
        raise Exception("Could not download model. [HTTP Error] {code}: {reason}."
                        .format(code=e.code, reason=e.reason))
    except URLError as e:
        raise Exception("Could not download model. [URL Error] {reason}."
                        .format(reason=e.reason))
