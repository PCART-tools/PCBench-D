def skip_code(code: types.CodeType):
    set_code_exec_strategy(
        code, FrameExecStrategy(FrameAction.SKIP, FrameAction.DEFAULT)
    )
