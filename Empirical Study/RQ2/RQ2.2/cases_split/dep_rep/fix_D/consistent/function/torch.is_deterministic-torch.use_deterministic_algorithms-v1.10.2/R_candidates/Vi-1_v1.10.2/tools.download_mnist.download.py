def download(destination_path: str, resource: str, quiet: bool) -> None:
    if os.path.exists(destination_path):
        if not quiet:
            print('{} already exists, skipping ...'.format(destination_path))
    else:
        for mirror in MIRRORS:
            url = mirror + resource
            print('Downloading {} ...'.format(url))
            try:
                hook = None if quiet else report_download_progress
                urlretrieve(url, destination_path, reporthook=hook)
            except (URLError, ConnectionError) as e:
                print('Failed to download (trying next):\n{}'.format(e))
                continue
            finally:
                if not quiet:
                    # Just a newline.
                    print()
            break
        else:
            raise RuntimeError('Error downloading resource!')
