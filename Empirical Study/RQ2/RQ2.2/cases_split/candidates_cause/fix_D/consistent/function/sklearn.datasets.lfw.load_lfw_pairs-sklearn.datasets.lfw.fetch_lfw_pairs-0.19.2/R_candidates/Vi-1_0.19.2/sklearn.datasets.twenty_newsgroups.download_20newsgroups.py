def download_20newsgroups(target_dir, cache_path):
    """Download the 20 newsgroups data and stored it as a zipped pickle."""
    train_path = os.path.join(target_dir, TRAIN_FOLDER)
    test_path = os.path.join(target_dir, TEST_FOLDER)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    logger.info("Downloading dataset from %s (14 MB)", ARCHIVE.url)
    archive_path = _fetch_remote(ARCHIVE, dirname=target_dir)

    logger.debug("Decompressing %s", archive_path)
    tarfile.open(archive_path, "r:gz").extractall(path=target_dir)
    os.remove(archive_path)

    # Store a zipped pickle
    cache = dict(train=load_files(train_path, encoding='latin1'),
                 test=load_files(test_path, encoding='latin1'))
    compressed_content = codecs.encode(pickle.dumps(cache), 'zlib_codec')
    with open(cache_path, 'wb') as f:
        f.write(compressed_content)

    shutil.rmtree(target_dir)
    return cache
