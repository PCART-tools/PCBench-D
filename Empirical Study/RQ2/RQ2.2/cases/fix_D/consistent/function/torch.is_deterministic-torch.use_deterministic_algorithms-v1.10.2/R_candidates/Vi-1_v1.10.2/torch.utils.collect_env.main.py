def main():
    print("Collecting environment information...")
    output = get_pretty_env_info()
    print(output)

    if TORCH_AVAILABLE and hasattr(torch, 'utils') and hasattr(torch.utils, '_crash_handler'):
        minidump_dir = torch.utils._crash_handler.DEFAULT_MINIDUMP_DIR
        if sys.platform == "linux" and os.path.exists(minidump_dir):
            dumps = [os.path.join(minidump_dir, dump) for dump in os.listdir(minidump_dir)]
            latest = max(dumps, key=os.path.getctime)
            ctime = os.path.getctime(latest)
            creation_time = datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')
            msg = "\n*** Detected a minidump at {} created on {}, ".format(latest, creation_time) + \
                  "if this is related to your bug please include it when you file a report ***"
            print(msg, file=sys.stderr)
