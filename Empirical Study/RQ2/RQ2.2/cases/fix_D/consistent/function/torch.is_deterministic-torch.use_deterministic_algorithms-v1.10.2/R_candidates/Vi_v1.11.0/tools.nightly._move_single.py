def _move_single(
    src: str,
    source_dir: str,
    target_dir: str,
    mover: Callable[[str, str], None],
    verb: str,
) -> None:
    is_dir = os.path.isdir(src)
    relpath = os.path.relpath(src, source_dir)
    trg = os.path.join(target_dir, relpath)
    _remove_existing(trg, is_dir)
    # move over new files
    if is_dir:
        os.makedirs(trg, exist_ok=True)
        for root, dirs, files in os.walk(src):
            relroot = os.path.relpath(root, src)
            for name in files:
                relname = os.path.join(relroot, name)
                s = os.path.join(src, relname)
                t = os.path.join(trg, relname)
                print(f"{verb} {s} -> {t}")
                mover(s, t)
            for name in dirs:
                relname = os.path.join(relroot, name)
                os.makedirs(os.path.join(trg, relname), exist_ok=True)
    else:
        print(f"{verb} {src} -> {trg}")
        mover(src, trg)
