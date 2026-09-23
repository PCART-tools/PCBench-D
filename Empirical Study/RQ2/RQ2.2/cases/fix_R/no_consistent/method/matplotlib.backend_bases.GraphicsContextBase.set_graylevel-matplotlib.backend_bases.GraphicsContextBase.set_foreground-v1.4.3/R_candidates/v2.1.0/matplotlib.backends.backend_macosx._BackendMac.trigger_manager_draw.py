    def trigger_manager_draw(manager):
        # For performance reasons, we don't want to redraw the figure after
        # each draw command. Instead, we mark the figure as invalid, so that it
        # will be redrawn as soon as the event loop resumes via PyOS_InputHook.
        # This function should be called after each draw event, even if
        # matplotlib is not running interactively.
        manager.canvas.invalidate()
