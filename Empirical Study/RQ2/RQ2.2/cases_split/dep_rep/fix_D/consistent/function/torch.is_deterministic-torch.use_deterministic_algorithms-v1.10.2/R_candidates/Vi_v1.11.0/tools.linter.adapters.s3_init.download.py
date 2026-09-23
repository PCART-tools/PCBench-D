def download(
    name: str,
    output_dir: str,
    url: str,
    reference_bin_hash: str,
) -> bool:
    """
    Download a platform-appropriate binary if one doesn't already exist at the expected location and verifies
    that it is the right binary by checking its SHA256 hash against the expected hash.
    """
    # First check if we need to do anything
    binary_path = Path(output_dir, name)
    if check(binary_path, reference_bin_hash):
        logging.info(f"Correct binary already exists at {binary_path}. Exiting.")
        return True

    # Create the output folder
    binary_path.parent.mkdir(parents=True, exist_ok=True)

    # Download the binary
    logging.info(f"Downloading {url} to {binary_path}")

    if DRY_RUN:
        logging.info("Exiting as there is nothing left to do in dry run mode")
        return True

    urllib.request.urlretrieve(
        url,
        binary_path,
        reporthook=report_download_progress if sys.stdout.isatty() else None,
    )

    logging.info(f"Downloaded {name} successfully.")

    # Check the downloaded binary
    if not check(binary_path, reference_bin_hash):
        logging.critical(f"Downloaded binary {name} failed its hash check")
        return False

    # Ensure that exeuctable bits are set
    mode = os.stat(binary_path).st_mode
    mode |= stat.S_IXUSR
    os.chmod(binary_path, mode)

    logging.info(f"Using {name} located at {binary_path}")
    return True
