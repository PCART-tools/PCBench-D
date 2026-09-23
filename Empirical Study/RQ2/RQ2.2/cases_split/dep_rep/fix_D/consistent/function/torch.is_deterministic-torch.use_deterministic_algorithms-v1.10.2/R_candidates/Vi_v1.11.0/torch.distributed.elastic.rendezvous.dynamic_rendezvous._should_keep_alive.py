def _should_keep_alive(ctx: _RendezvousContext) -> bool:
    """Determines whether a keep-alive heartbeat should be sent."""
    try:
        last_heartbeat = ctx.state.last_heartbeats[ctx.node]
    except KeyError:
        return False

    return last_heartbeat <= datetime.utcnow() - ctx.settings.keep_alive_interval
