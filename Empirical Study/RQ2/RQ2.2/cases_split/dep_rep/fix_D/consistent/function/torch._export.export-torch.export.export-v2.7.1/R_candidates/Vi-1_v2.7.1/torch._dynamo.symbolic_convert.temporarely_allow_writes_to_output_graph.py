@contextlib.contextmanager
def temporarely_allow_writes_to_output_graph(tx: "InstructionTranslatorBase"):
    try:
        tmp = tx.output.should_exit
        tx.output.should_exit = False
        yield
    finally:
        tx.output.should_exit = tmp
