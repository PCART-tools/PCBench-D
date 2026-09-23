class CommunicatorContext:
    """A context controlling collective communicator initialization and finalization."""

    def __init__(self, **args: _ArgVals) -> None:
        self.args = args
        key = "dmlc_nccl_path"
        if args.get(key, None) is not None:
            return

        binfo = build_info()
        if not binfo["USE_DLOPEN_NCCL"]:
            return

        try:
            # PyPI package of NCCL.
            from nvidia.nccl import lib

            # There are two versions of nvidia-nccl, one is from PyPI, another one from
            # nvidia-pyindex. We support only the first one as the second one is too old
            # (2.9.8 as of writing).
            if lib.__file__ is not None:
                dirname: Optional[str] = os.path.dirname(lib.__file__)
            else:
                dirname = None

            if dirname:
                path = os.path.join(dirname, "libnccl.so.2")
                self.args[key] = path
        except ImportError:
            pass

    def __enter__(self) -> _Args:
        init(**self.args)
        assert is_distributed()
        LOGGER.debug("-------------- communicator say hello ------------------")
        return self.args

    def __exit__(self, *args: Any) -> None:
        finalize()
        LOGGER.debug("--------------- communicator say bye ------------------")
