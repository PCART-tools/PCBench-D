def download_bin(name: str, output_dir: str, platform_to_url: Dict[str, str]) -> bool:
    """
    Downloads the binary appropriate for the host platform and stores it in the given output directory.
    """
    if HOST_PLATFORM not in platform_to_url:
        print(f"Unsupported platform: {HOST_PLATFORM}", file=sys.stderr)
        return False

    url = platform_to_url[HOST_PLATFORM]
    filename = os.path.join(output_dir, name)

    # Try to download binary.
    print(f"Downloading {name} to {output_dir}", file=sys.stderr)
    try:
        urllib.request.urlretrieve(
            url,
            filename,
            reporthook=report_download_progress if sys.stdout.isatty() else None,
        )
    except urllib.error.URLError as e:
        print(f"Error downloading {filename}: {e}", file=sys.stderr)
        return False
    finally:
        print(file=sys.stderr)

    return True
