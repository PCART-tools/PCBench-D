def _remove_existing(trg: str, is_dir: bool) -> None:
    if os.path.exists(trg):
        if is_dir:
            shutil.rmtree(trg)
        else:
            os.remove(trg)
