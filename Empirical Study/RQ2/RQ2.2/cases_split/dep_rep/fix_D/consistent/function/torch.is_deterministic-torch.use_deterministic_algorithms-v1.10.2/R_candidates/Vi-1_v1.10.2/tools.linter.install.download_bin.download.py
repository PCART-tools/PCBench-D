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
            print(f"Unable to create directory for {name} binary: {output_dir}")
            return False
        finally:
            if verbose:
                print(f"Created directory {output_dir} for {name} binary")

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
                print(f"Found pre-existing {name} binary, skipping download")

    # Now that the binary is where it should be, hash it.
    actual_bin_hash = compute_file_sha256(output_path)

    # If the host platform is not in platform_to_hash, it is unsupported.
    if HOST_PLATFORM not in platform_to_hash:
        print(f"Unsupported platform: {HOST_PLATFORM}")
        return False

    # This is the path to the file containing the reference hash.
    hashpath = os.path.join(PYTORCH_ROOT, platform_to_hash[HOST_PLATFORM])

    if not os.path.exists(hashpath):
        print("Unable to find reference binary hash")
        return False

    # Load the reference hash and compare the actual hash to it.
    with open(hashpath, "r") as f:
        reference_bin_hash = f.readline().strip()

        if verbose:
            print(f"Reference Hash: {reference_bin_hash}")
            print(f"Actual Hash: {repr(actual_bin_hash)}")

        if reference_bin_hash != actual_bin_hash:
            print("The downloaded binary is not what was expected!")
            print(f"Downloaded hash: {repr(actual_bin_hash)} vs expected {reference_bin_hash}")

            # Err on the side of caution and try to delete the downloaded binary.
            try:
                os.unlink(output_path)
                print("The binary has been deleted just to be safe")
            except OSError as e:
                print(f"Failed to delete binary: {e}")
                print("Delete this binary as soon as possible and do not execute it!")

            return False
        else:
            # Make sure the binary is executable.
            mode = os.stat(output_path).st_mode
            mode |= stat.S_IXUSR
            os.chmod(output_path, mode)
            print(f"Using {name} located at {output_path}")

    return True
