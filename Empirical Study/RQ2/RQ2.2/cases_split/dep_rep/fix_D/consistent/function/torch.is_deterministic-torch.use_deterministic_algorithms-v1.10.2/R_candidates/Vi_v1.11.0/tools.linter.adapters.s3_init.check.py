def check(binary_path: Path, reference_hash: str) -> bool:
    """Check whether the binary exists and is the right one.

    If there is hash difference, delete the actual binary.
    """
    if not binary_path.exists():
        logging.info(f"{binary_path} does not exist.")
        return False

    existing_binary_hash = compute_file_sha256(str(binary_path))
    if existing_binary_hash == reference_hash:
        return True

    logging.warning(
        textwrap.dedent(
            f"""\
            Found binary hash does not match reference!

            Found hash: {existing_binary_hash}
            Reference hash: {reference_hash}

            Deleting {binary_path} just to be safe.
            """
        )
    )
    if DRY_RUN:
        logging.critical(
            "In dry run mode, so not actually deleting the binary. But consider deleting it ASAP!"
        )
        return False

    try:
        binary_path.unlink()
    except OSError as e:
        logging.critical(f"Failed to delete binary: {e}")
        logging.critical(
            "Delete this binary as soon as possible and do not execute it!"
        )

    return False
