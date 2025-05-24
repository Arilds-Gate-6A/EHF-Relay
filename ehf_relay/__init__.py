from ehf_relay.parse import parse

def run(source, target):
    for message_text in source():
        message = parse(message_text)
        target(message)