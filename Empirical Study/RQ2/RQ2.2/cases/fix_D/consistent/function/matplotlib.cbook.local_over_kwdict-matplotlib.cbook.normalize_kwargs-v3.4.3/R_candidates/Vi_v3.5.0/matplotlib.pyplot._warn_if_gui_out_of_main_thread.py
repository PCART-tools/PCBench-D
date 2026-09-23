def _warn_if_gui_out_of_main_thread():
    if (_get_required_interactive_framework(_backend_mod)
            and threading.current_thread() is not threading.main_thread()):
        _api.warn_external(
            "Starting a Matplotlib GUI outside of the main thread will likely "
            "fail.")
