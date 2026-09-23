def simplify(report: Report) -> SimplerReport:
    if 'format_version' not in report:  # version 1 implicitly
        v1report = cast(Version1Report, report)
        return {
            # we just don't have test filename information sadly, so we
            # just make one fake filename that is the empty string
            '': {
                suite_name: {
                    # This clobbers some cases that have duplicate names
                    # because in version 1, we would merge together all
                    # the suites with a given name (even if they came
                    # from different files), so there were actually
                    # situations in which two cases in the same suite
                    # shared a name (because they actually originally
                    # came from two suites that were then merged). It
                    # would probably be better to warn about the cases
                    # that we're silently discarding here, but since
                    # we're only uploading in the new format (where
                    # everything is also keyed by filename) going
                    # forward, it shouldn't matter too much.
                    case['name']: newify_case(case)
                    for case in suite['cases']
                }
                for suite_name, suite in v1report['suites'].items()
            }
        }
    else:
        v_report = cast(VersionedReport, report)
        version = v_report['format_version']
        if version == 2:
            v2report = cast(Version2Report, v_report)
            return {
                filename: {
                    suite_name: suite['cases']
                    for suite_name, suite in file_data['suites'].items()
                }
                for filename, file_data in v2report['files'].items()
            }
        else:
            raise RuntimeError(f'Unknown format version: {version}')
