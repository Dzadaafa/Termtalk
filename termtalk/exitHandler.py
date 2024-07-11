import signal

def stop_handler(signum, frame, cleanup_callback):
    cleanup_callback()

def start(cleanup_callback):
    # Register the signal handler and pass the cleanup callback
    signal.signal(signal.SIGINT, lambda signum, frame: stop_handler(signum, frame, cleanup_callback))
