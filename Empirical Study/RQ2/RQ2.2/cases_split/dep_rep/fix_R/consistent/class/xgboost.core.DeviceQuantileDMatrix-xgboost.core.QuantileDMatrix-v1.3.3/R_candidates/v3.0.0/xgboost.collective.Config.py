@dataclass
class Config:
    """User configuration for the communicator context. This is used for easier
    integration with distributed frameworks. Users of the collective module can pass the
    parameters directly into tracker and the communicator.

    .. versionadded:: 3.0

    Attributes
    ----------
    retry : See `dmlc_retry` in :py:meth:`init`.

    timeout :
        See `dmlc_timeout` in :py:meth:`init`. This is only used for communicators, not
        the tracker. They are different parameters since the timeout for tracker limits
        only the time for starting and finalizing the communication group, whereas the
        timeout for communicators limits the time used for collective operations.

    tracker_host_ip : See :py:class:`~xgboost.tracker.RabitTracker`.

    tracker_port : See :py:class:`~xgboost.tracker.RabitTracker`.

    tracker_timeout : See :py:class:`~xgboost.tracker.RabitTracker`.

    """

    retry: Optional[int] = None
    timeout: Optional[int] = None

    tracker_host_ip: Optional[str] = None
    tracker_port: Optional[int] = None
    tracker_timeout: Optional[int] = None

    def get_comm_config(self, args: _Args) -> _Args:
        """Update the arguments for the communicator."""
        if self.retry is not None:
            args["dmlc_retry"] = self.retry
        if self.timeout is not None:
            args["dmlc_timeout"] = self.timeout
        return args
