    @classmethod
    def _init_from_registry(cls):
        if sys.platform != 'win32' or rcParams[cls.exec_key] != 'convert':
            return
        from six.moves import winreg
        for flag in (0, winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY):
            try:
                hkey = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE,
                                        'Software\\Imagemagick\\Current',
                                        0, winreg.KEY_QUERY_VALUE | flag)
                binpath = winreg.QueryValueEx(hkey, 'BinPath')[0]
                winreg.CloseKey(hkey)
                binpath += '\\convert.exe'
                break
            except Exception:
                binpath = ''
        rcParams[cls.exec_key] = rcParamsDefault[cls.exec_key] = binpath
