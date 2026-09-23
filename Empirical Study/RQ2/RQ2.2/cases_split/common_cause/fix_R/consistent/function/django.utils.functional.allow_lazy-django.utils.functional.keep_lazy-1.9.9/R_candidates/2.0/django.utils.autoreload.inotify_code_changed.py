def inotify_code_changed():
    """
    Check for changed code using inotify. After being called
    it blocks until a change event has been fired.
    """
    class EventHandler(pyinotify.ProcessEvent):
        modified_code = None

        def process_default(self, event):
            if event.path.endswith('.mo'):
                EventHandler.modified_code = I18N_MODIFIED
            else:
                EventHandler.modified_code = FILE_MODIFIED

    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, EventHandler())

    def update_watch(sender=None, **kwargs):
        if sender and getattr(sender, 'handles_files', False):
            # No need to update watches when request serves files.
            # (sender is supposed to be a django.core.handlers.BaseHandler subclass)
            return
        mask = (
            pyinotify.IN_MODIFY |
            pyinotify.IN_DELETE |
            pyinotify.IN_ATTRIB |
            pyinotify.IN_MOVED_FROM |
            pyinotify.IN_MOVED_TO |
            pyinotify.IN_CREATE |
            pyinotify.IN_DELETE_SELF |
            pyinotify.IN_MOVE_SELF
        )
        for path in gen_filenames(only_new=True):
            wm.add_watch(path, mask)

    # New modules may get imported when a request is processed.
    request_finished.connect(update_watch)

    # Block until an event happens.
    update_watch()
    notifier.check_events(timeout=None)
    notifier.read_events()
    notifier.process_events()
    notifier.stop()

    # If we are here the code must have changed.
    return EventHandler.modified_code
