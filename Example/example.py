from sys import stdin
from os import getcwd, path
import asyncio, signal
from asyncio.subprocess import PIPE, Process


class ExampleAPI:
    process:Process
    async def start_comlink(_):
        _.process = await asyncio.create_subprocess_exec(
            'python', path.join('src', 'comlink.py'), getcwd(),
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
        )


    async def handle_comlink_input(_):
        loop = asyncio.get_event_loop()
        while True:
            line = await loop.run_in_executor(None, stdin.readline)
            if not line: continue
            if line == 'stop':
                _.process.stdin.write('close\n')
                break
            _.process.stdin.write(line.encode())
            await _.process.stdin.drain()


    async def handle_comlink_output(_):
        while True:
            err = await _.process.stderr.readline()
            if err:
                print(f"[DEBUG] {err.decode().strip()}")
                continue

            line = await _.process.stdout.readline()
            line = line.decode()
            if not line:break
            if line.startswith("~"):
                print(f"[Comment]: {line}")
            else:
                print(f"[REPLY]: {line}")


    async def main(_):
        print("Starting ExampleAPI")
        await _.start_comlink()
        print("Gathering...")
        await asyncio.gather(
            _.handle_comlink_output(),
            _.handle_comlink_input(),
        )
        print("Closing ExampleAPI...")


    async def send_comment():
        pass


    def send_stop(_, param1, param2):
        print(f"{param1}, {param2}")
        _.process.stdin.write('close\n'.encode())
        exit(1)
    

instance = ExampleAPI()

signal.signal(signal.SIGINT, instance.send_stop)
signal.signal(signal.SIGTERM, instance.send_stop)

# run the api as an asynchronous process
asyncio.run(instance.main())
