def jython_reloader(main_func, args, kwargs):
    from _systemrestart import SystemRestart
    _thread.start_new_thread(main_func, args)
    while True:
        if code_changed():
            raise SystemRestart
        time.sleep(1)
