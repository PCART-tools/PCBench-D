def download_bin(name: str, output_dir: str, platform_to_url: Dict[str, str]) -> bool:
    """
    Downloads the binary appropriate for the host platform and stores it in the given output directory.
    """
    if HOST_PLATFORM not in platform_to_url:
        print(f"Unsupported platform: {HOST_PLATFORM}")
        return False

    url = platform_to_url[HOST_PLATFORM]
    filename = os.path.join(output_dir, name)

    # Try to download binary.
    print(f"Downloading {name} to {output_dir}")
    try:
        urllib.request.urlretrieve(
            url,
            filename,
            reporthook=report_download_progress if sys.stdout.isatty() else None,
        )
    except urllib.error.URLError as e:
        print(f"Error downloading {filename}: {e}")
        return False
    finally:
        print()

    return True
