    def handle_error(self, request, status=500, exc=None, message=None):
        """Handle errors.

        Returns HTTP response with specific status code. Logs additional
        information. It always closes current connection."""
        self.log_exception("Error handling request", exc_info=exc)

        if status == 500:
            msg = "<h1>500 Internal Server Error</h1>"
            if self.debug:
                with suppress(Exception):
                    tb = traceback.format_exc()
                    tb = html_escape(tb)
                    msg += '<br><h2>Traceback:</h2>\n<pre>'
                    msg += tb
                    msg += '</pre>'
            else:
                msg += "Server got itself in trouble"
                msg = ("<html><head><title>500 Internal Server Error</title>"
                       "</head><body>" + msg + "</body></html>")
        else:
            msg = message

        resp = Response(status=status, text=msg, content_type='text/html')
        resp.force_close()

        # some data already got sent, connection is broken
        if request.writer.output_size > 0 or self.transport is None:
            self.force_close()

        return resp
