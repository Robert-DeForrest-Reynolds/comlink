from sys import argv, stdin, stdout, stderr


def log(msg): print(f'{msg}\n', file=stderr, flush=True)


workspace_path = argv[1]
tracker = 0

test_comments = {
}


log("comlink.py is running...")
log(f'Workspace: {workspace_path}')


def create_comment(comment) -> None:
    global tracker
    log(f"Creating comment: {comment}")
    comment_id = tracker
    stdout.write(f'~{comment_id}')
    stdout.flush()
    test_comments.update({str(tracker):comment})
    tracker += 1


while True:
    line = stdin.readline().strip()
    if not line:
        continue
    if line[0] == '~':
        create_comment(line[1:])
    if line in test_comments:
        stdout.write(f'{test_comments[line]}\n')
        stdout.flush()
        log(f'Received ID: {line}')