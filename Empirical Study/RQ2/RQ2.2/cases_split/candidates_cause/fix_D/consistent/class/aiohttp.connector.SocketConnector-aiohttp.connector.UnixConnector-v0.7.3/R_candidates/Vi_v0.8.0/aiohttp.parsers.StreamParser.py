class StreamParser:
    """StreamParser manages incoming bytes stream and protocol parsers.

    StreamParser uses ParserBuffer as internal buffer.

    set_parser() sets current parser, it creates DataQueue object
    and sends ParserBuffer and DataQueue into parser generator.

    unset_parser() sends EofStream into parser and then removes it.
    """

    def __init__(self, *, loop=None, buf=None,
                 paused=True, limit=DEFAULT_LIMIT):
        self._loop = loop
        self._eof = False
        self._exception = None
        self._parser = None
        self._transport = None
        self._limit = limit
        self._paused = False
        self._stream_paused = paused
        self._output = None
        self._buffer = buf if buf is not None else ParserBuffer()

    @property
    def output(self):
        return self._output

    def set_transport(self, transport):
        assert self._transport is None, 'Transport already set'
        self._transport = transport

    def at_eof(self):
        return self._eof

    def pause_stream(self):
        self._stream_paused = True

    def resume_stream(self):
        if self._paused and self._buffer.size <= self._limit:
            self._paused = False
            self._transport.resume_reading()

        self._stream_paused = False
        if self._parser and self._buffer:
            self.feed_data(b'')

    def exception(self):
        return self._exception

    def set_exception(self, exc):
        self._exception = exc

        if self._output is not None:
            self._output.set_exception(exc)
            self._output = None
            self._parser = None

    def feed_data(self, data):
        """send data to current parser or store in buffer."""
        if data is None:
            return

        if self._parser and not self._stream_paused:
            try:
                self._parser.send(data)
            except StopIteration:
                self._output.feed_eof()
                self._output = None
                self._parser = None
            except Exception as exc:
                self._output.set_exception(exc)
                self._output = None
                self._parser = None
        else:
            self._buffer.feed_data(data)

        if (self._transport is not None and not self._paused and
                self._buffer.size > 2*self._limit):
            try:
                self._transport.pause_reading()
            except NotImplementedError:
                # The transport can't be paused.
                # We'll just have to buffer all data.
                # Forget the transport so we don't keep trying.
                self._transport = None
            else:
                self._paused = True

    def feed_eof(self):
        """send eof to all parsers, recursively."""
        if self._parser:
            try:
                if self._buffer:
                    self._parser.send(b'')
                self._parser.throw(EofStream())
            except StopIteration:
                self._output.feed_eof()
            except EofStream:
                self._output.set_exception(errors.ConnectionError())
            except Exception as exc:
                self._output.set_exception(exc)

            self._parser = None
            self._output = None

        self._buffer.shrink()
        self._eof = True

    def set_parser(self, parser):
        """set parser to stream. return parser's DataQueue."""
        if self._parser:
            self.unset_parser()

        output = DataQueue(self, loop=self._loop)
        if self._exception:
            output.set_exception(self._exception)
            return output

        # init parser
        p = parser(output, self._buffer)
        assert inspect.isgenerator(p), 'Generator is required'

        try:
            # initialize parser with data and parser buffers
            next(p)
        except StopIteration:
            pass
        except Exception as exc:
            output.set_exception(exc)
        else:
            # parser still require more data
            self._parser = p
            self._output = output

            if self._eof:
                self.unset_parser()

        return output

    def unset_parser(self):
        """unset parser, send eof to the parser and then remove it."""
        if self._buffer:
            self._buffer.shrink()

        if self._parser is None:
            return

        try:
            self._parser.throw(EofStream())
        except StopIteration:
            self._output.feed_eof()
        except EofStream:
            self._output.set_exception(errors.ConnectionError())
        except Exception as exc:
            self._output.set_exception(exc)
        finally:
            self._output = None
            self._parser = None
