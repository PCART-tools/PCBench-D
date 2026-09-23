    @classmethod
    def _run_checked_subprocess(cls, command, tex, *, cwd=None):
        _log.debug(cbook._pformat_subprocess(command))
        try:
            report = subprocess.check_output(
                command, cwd=cwd if cwd is not None else cls.texcache,
                stderr=subprocess.STDOUT)
        except FileNotFoundError as exc:
            raise RuntimeError(
                'Failed to process string with tex because {} could not be '
                'found'.format(command[0])) from exc
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                '{prog} was not able to process the following string:\n'
                '{tex!r}\n\n'
                'Here is the full command invocation and its output:\n\n'
                '{format_command}\n\n'
                '{exc}\n\n'.format(
                    prog=command[0],
                    format_command=cbook._pformat_subprocess(command),
                    tex=tex.encode('unicode_escape'),
                    exc=exc.output.decode('utf-8', 'backslashreplace'))
                ) from None
        _log.debug(report)
        return report
