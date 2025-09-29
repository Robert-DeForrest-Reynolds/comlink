from sys import stderr

def log(msg): print(f'{msg}\n', file=stderr, flush=True)