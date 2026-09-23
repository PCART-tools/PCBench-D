    def _start_event_axes_interaction(self, event, *, method):

        def _ax_filter(ax):
            return (ax.in_axes(event) and
                    ax.get_navigate() and
                    getattr(ax, f"can_{method}")()
                    )

        def _capture_events(ax):
            f = ax.get_forward_navigation_events()
            if f == "auto":  # (capture = patch visibility)
                f = not ax.patch.get_visible()
            return not f

        # get all relevant axes for the event
        axes = list(filter(_ax_filter, self.canvas.figure.get_axes()))

        if len(axes) == 0:
            return []

        if self._nav_stack() is None:
            self.push_current()   # Set the home button to this view.

        # group axes by zorder (reverse to trigger later axes first)
        grps = dict()
        for ax in reversed(axes):
            grps.setdefault(ax.get_zorder(), []).append(ax)

        axes_to_trigger = []
        # go through zorders in reverse until we hit a capturing axes
        for zorder in sorted(grps, reverse=True):
            for ax in grps[zorder]:
                axes_to_trigger.append(ax)
                # NOTE: shared axes are automatically triggered, but twin-axes not!
                axes_to_trigger.extend(ax._twinned_axes.get_siblings(ax))

                if _capture_events(ax):
                    break  # break if we hit a capturing axes
            else:
                # If the inner loop finished without an explicit break,
                # (e.g. no capturing axes was found) continue the
                # outer loop to the next zorder.
                continue

            # If the inner loop was terminated with an explicit break,
            # terminate the outer loop as well.
            break

        # avoid duplicated triggers (but keep order of list)
        axes_to_trigger = list(dict.fromkeys(axes_to_trigger))

        return axes_to_trigger
