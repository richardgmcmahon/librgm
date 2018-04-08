def mk_timestamp():
    """

    ISO timestamp

    """
    import time

    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())

    return timestamp
