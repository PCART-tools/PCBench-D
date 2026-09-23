def StartImmediate(i_know=False):
    global _immediate_mode
    global _immediate_root_folder
    if IsImmediate():
        # already in immediate mode. We will kill the previous one
        # and start from fresh.
        StopImmediate()
    _immediate_mode = True
    with WorkspaceGuard(_immediate_workspace_name):
        _immediate_root_folder = tempfile.mkdtemp()
        ResetWorkspace(_immediate_root_folder)
    if i_know:
        # if the user doesn't want to see the warning message, sure...
        return
    print("""
    Enabling immediate mode in caffe2 python is an EXTREMELY EXPERIMENTAL
    feature and may very easily go wrong. This is because Caffe2 uses a
    declarative way of defining operators and models, which is essentially
    not meant to run things in an interactive way. Read the following carefully
    to make sure that you understand the caveats.

    (1) You need to make sure that the sequences of operators you create are
    actually runnable sequentially. For example, if you create an op that takes
    an input X, somewhere earlier you should have already created X.

    (2) Caffe2 immediate uses one single workspace, so if the set of operators
    you run are intended to be under different workspaces, they will not run.
    To create boundaries between such use cases, you can call FinishImmediate()
    and StartImmediate() manually to flush out everything no longer needed.

    (3) Underlying objects held by the immediate mode may interfere with your
    normal run. For example, if there is a leveldb that you opened in immediate
    mode and did not close, your main run will fail because leveldb does not
    support double opening. Immediate mode may also occupy a lot of memory esp.
    on GPUs. Call FinishImmediate() as soon as possible when you no longer
    need it.

    (4) Immediate is designed to be slow. Every immediate call implicitly
    creates a temp operator object, runs it, and destroys the operator. This
    slow-speed run is by design to discourage abuse. For most use cases other
    than debugging, do NOT turn on immediate mode.

    (5) If there is anything FATAL happening in the underlying C++ code, the
    immediate mode will immediately (pun intended) cause the runtime to crash.

    Thus you should use immediate mode with extra care. If you still would
    like to, have fun [https://xkcd.com/149/].
    """)
