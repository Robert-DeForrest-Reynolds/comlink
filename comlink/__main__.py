if __name__ != '__main__':
    from sys import exit
    print("comlink/__main__ cannot be imported")
    exit(1)


from comlink import comlink

_ = comlink()