    @staticmethod
    def _cleanup_remaining_instances():
        unclean_instances = list(LatexManager._unclean_instances)
        for latex_manager in unclean_instances:
            latex_manager._cleanup()
