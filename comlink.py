from sys import argv, stdout, stderr

stdout.write("running comlink.py")
stdout.flush()

test_comments = {
    12348:"I'm a comment"
}

for arg in argv:
    print(arg)