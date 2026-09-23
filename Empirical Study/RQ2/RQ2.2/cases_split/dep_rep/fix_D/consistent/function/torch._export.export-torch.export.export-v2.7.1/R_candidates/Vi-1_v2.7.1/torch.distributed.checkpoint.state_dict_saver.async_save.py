@_dcp_method_logger(log_exceptions=True)
def async_save(
    state_dict: STATE_DICT_TYPE,
    *,
    checkpoint_id: Union[str, os.PathLike, None] = None,
    storage_writer: Optional[StorageWriter] = None,
    planner: Optional[SavePlanner] = None,
    process_group: Optional[dist.ProcessGroup] = None,
    async_checkpointer_type: AsyncCheckpointerType = AsyncCheckpointerType.THREAD,
) -> Future:
    """Asynchronous version of ``save``. This code first de-stages the state_dict on to the
    staging storage (defaults to CPU memory), and then calls the `save` in a separate thread.

    .. warning::
        This feature is experimental and subject to change.

    Args:
        state_dict (Dict[str, Any]): The state_dict to save.
        checkpoint_id (Union[str, os.PathLike, None]):
            The ID of this checkpoint instance. The meaning of the checkpoint_id
            depends on the storage. It can be a path to a folder or to a file.
            It can also be a key if the storage is a key-value store.
            (Default: ``None``)
        storage_writer (Optional[StorageWriter]):
            Instance of StorageWriter used to perform 'stage' and  'save'. If
            this is not specified, DCP will automatically infer the writer based on the
            checkpoint_id. If checkpoint_id is also None, an exception will
            be raised. (Default: ``None``)
        planner (Optional[SavePlanner]):
            Instance of SavePlanner. If this is not specificed, the default
            planner will be used. (Default: ``None``)
        process_group (Optional[ProcessGroup]):
            ProcessGroup to be used for cross-rank synchronization.
            (Default: ``None``)

    Returns:
        Future: A future holding the resultant Metadata object from `save`.

    Example:
        >>> # xdoctest: +SKIP
        >>> my_model = MyModule()

        >>> state_dict = {"model": my_model}

        >>> fs_storage_writer = torch.distributed.checkpoint.FileSystemWriter(
        ...     "/checkpoint/1"
        ... )
        >>> checkpoint_future = torch.distributed.checkpoint.async_save(
        >>>     state_dict=state_dict,
        >>>     storage_writer=fs_storage_writer,
        >>> )
        >>>
        >>> # ... do some work ...
        >>>
        >>> checkpoint_future.result()

    """
    torch._C._log_api_usage_once("torch.distributed.checkpoint.async_save")

    if dist.is_available() and dist.is_initialized():
        pg = process_group or _get_default_group()
        assert (
            torch.device("cpu") in pg._device_types  # type: ignore[attr-defined]
        ), (
            "A CPU backend must be enabled for async save; try initializing process group with 'cpu:gloo,cuda:nccl'"
        )

    storage_writer = cast(
        StorageWriter, _storage_setup(storage_writer, checkpoint_id, reader=False)
    )

    state_dict = _stateful_to_state_dict(state_dict)
    if isinstance(storage_writer, AsyncStager):
        staged_state_dict = storage_writer.stage(state_dict)
    else:  # provides bwc for storage_writers not implementing AsyncStager
        staged_state_dict = _create_cpu_state_dict(state_dict)
        _copy_state_dict(state_dict, staged_state_dict, type_check=False)

    executor: _AsyncCheckpointExecutor = (
        _ProcessBasedAsyncCheckpointExecutor()
        if async_checkpointer_type == AsyncCheckpointerType.PROCESS
        else _ThreadBasedAsyncCheckpointExecutor()
    )

    f: Future = executor.execute_save(
        staged_state_dict,
        checkpoint_id=checkpoint_id,
        storage_writer=storage_writer,
        planner=planner,
        process_group=process_group,
    )

    if (
        isinstance(storage_writer, AsyncStager)
        and storage_writer.should_synchronize_after_execute
    ):
        storage_writer.synchronize_staging()

    return f
