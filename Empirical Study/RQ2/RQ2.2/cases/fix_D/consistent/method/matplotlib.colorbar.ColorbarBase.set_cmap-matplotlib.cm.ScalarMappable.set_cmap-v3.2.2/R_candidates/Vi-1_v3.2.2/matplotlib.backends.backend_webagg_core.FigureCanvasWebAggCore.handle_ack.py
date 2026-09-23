    def handle_ack(self, event):
        # Network latency tends to decrease if traffic is flowing
        # in both directions.  Therefore, the browser sends back
        # an "ack" message after each image frame is received.
        # This could also be used as a simple sanity check in the
        # future, but for now the performance increase is enough
        # to justify it, even if the server does nothing with it.
        pass
