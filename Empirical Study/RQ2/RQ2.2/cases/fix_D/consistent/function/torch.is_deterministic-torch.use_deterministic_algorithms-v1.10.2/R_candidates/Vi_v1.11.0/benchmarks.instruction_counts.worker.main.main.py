def main(communication_file: str) -> None:
    result: Union[WorkerOutput, WorkerFailure]
    try:
        with open(communication_file, "rb") as f:
            timer_args: WorkerTimerArgs = WorkerUnpickler(f).load_input()
            assert isinstance(timer_args, WorkerTimerArgs)
        result = _run(timer_args)

    except KeyboardInterrupt:
        # Runner process sent SIGINT.
        sys.exit()

    except BaseException:
        trace_f = io.StringIO()
        traceback.print_exc(file=trace_f)
        result = WorkerFailure(failure_trace=trace_f.getvalue())

    if not os.path.exists(os.path.split(communication_file)[0]):
        # This worker is an orphan, and the parent has already cleaned up the
        # working directory. In that case we can simply exit.
        print(f"Orphaned worker {os.getpid()} exiting.")
        return

    with open(communication_file, "wb") as f:
        pickle.dump(result, f)
