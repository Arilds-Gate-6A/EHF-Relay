def _parse(xml):
    pass

def run(source, target):
    for message_text in source():
        message = _parse(message_text)
        target(message)