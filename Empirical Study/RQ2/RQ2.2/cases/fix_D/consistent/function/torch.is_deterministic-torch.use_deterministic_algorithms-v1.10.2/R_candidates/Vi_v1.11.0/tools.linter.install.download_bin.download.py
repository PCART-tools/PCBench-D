def download(
    name: str,
    output_dir: str,
    platform_to_url: Dict[str, str],
    platform_to_hash: Dict[str, str],
    verbose: bool = False,
) -> bool:
    """
    Download a platform-appropriate binary if one doesn't already exist at the expected location and verifies
    that it is the right binary by checking its SHA256 hash against the expected hash.
    """

    output_path = os.path.join(output_dir, name)
    if not os.path.exists(output_dir):
        # If the directory doesn't exist, try to create it.
        try:
            os.mkdir(output_dir)
        except OSError as e:
            print(f"Unable to create directory for {name} binary: {output_dir}", file=sys.stderr)
            return False
        finally:
            if verbose:
                print(f"Created directory {output_dir} for {name} binary", file=sys.stderr)

        # If the directory didn't exist, neither did the binary, so download it.
        ok = download_bin(name, output_dir, platform_to_url)

        if not ok:
            return False
    else:
        # If the directory exists but the binary doesn't, download it.
        if not os.path.exists(output_path):
            ok = download_bin(name, output_dir, platform_to_url)

            if not ok:
                return False
        else:
            if verbose:
                print(f"Found pre-existing {name} binary, skipping download", file=sys.stderr)

    # Now that the binary is where it should be, hash it.
    actual_bin_hash = compute_file_sha256(output_path)

    # If the host platform is not in platform_to_hash, it is unsupported.
    if HOST_PLATFORM not in platform_to_hash:
        print(f"Unsupported platform: {HOST_PLATFORM}", file=sys.stderr)
        return False

    # This is the path to the file containing the reference hash.
    hashpath = os.path.join(PYTORCH_ROOT, platform_to_hash[HOST_PLATFORM])

    if not os.path.exists(hashpath):
        print("Unable to find reference binary hash", file=sys.stderr)
        return False

    # Load the reference hash and compare the actual hash to it.
    with open(hashpath, "r") as f:
        reference_bin_hash = f.readline().strip()

        if verbose:
            print(f"Reference Hash: {reference_bin_hash}", file=sys.stderr)
            print(f"Actual Hash: {repr(actual_bin_hash)}", file=sys.stderr)

        if reference_bin_hash != actual_bin_hash:
            print("The downloaded binary is not what was expected!", file=sys.stderr)
            print(f"Downloaded hash: {repr(actual_bin_hash)} vs expected {reference_bin_hash}", file=sys.stderr)

            # Err on the side of caution and try to delete the downloaded binary.
            try:
                os.unlink(output_path)
                print("The binary has been deleted just to be safe", file=sys.stderr)
            except OSError as e:
                print(f"Failed to delete binary: {e}", file=sys.stderr)
                print("Delete this binary as soon as possible and do not execute it!", file=sys.stderr)

            return False
        else:
            # Make sure the binary is executable.
            mode = os.stat(output_path).st_mode
            mode |= stat.S_IXUSR
            os.chmod(output_path, mode)
            print(f"Using {name} located at {output_path}", file=sys.stderr)

    return True
