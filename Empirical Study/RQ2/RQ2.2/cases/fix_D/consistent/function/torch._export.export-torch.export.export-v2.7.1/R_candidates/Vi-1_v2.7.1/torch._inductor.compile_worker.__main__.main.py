def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--pickler", type=functools.partial(_lookup_and_create_type, SubprocPickler)
        )
        parser.add_argument("--kind", type=SubprocKind)
        parser.add_argument("--workers", type=int)
        parser.add_argument("--parent", type=int)
        parser.add_argument("--read-fd", type=int)
        parser.add_argument("--write-fd", type=int)
        args = parser.parse_args()
        if os.getppid() != args.parent:
            sys.exit(0)
        read_fd = os.fdopen(args.read_fd, "rb")
        write_fd = os.fdopen(args.write_fd, "wb")

        pre_fork_setup()

        _async_compile_initializer(args.parent)

        SubprocMain(args.pickler, args.kind, args.workers, read_fd, write_fd).main()
    except Exception:
        log.exception("Uncaught exception in compile_worker subprocess")
