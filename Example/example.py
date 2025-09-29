from sys import stdin
from os import getcwd, path, killpg, getpgid, _exit
import asyncio, signal
from asyncio.subprocess import PIPE, Process


class ExampleAPI:
    process:Process
    event_loop:asyncio.AbstractEventLoop


    def __init__(_):
        _.stopping = False


    async def start_comlink(_):
        _.process = await asyncio.create_subprocess_exec(
            'python', '-u', path.join('src', 'comlink.py'), getcwd(),
            stdin=PIPE, stdout=PIPE, stderr=PIPE,
        )


    async def handle_comlink(_):
        while True:
            line:str = await _.loop.run_in_executor(None, stdin.readline)
            if not line: continue
            _.process.stdin.write((line + "\n").encode())
            await _.process.stdin.drain()


            line = await _.process.stderr.readline()
            if not line and line != '\n': break
            if line: print(f"[ERROR]: {line}")

            line = await _.process.stdout.readline()
            if not line: break
            line = line.decode()
            if line.startswith("~"): print(f"[OUTPUT]: {line}")
            else: print(f"[REPLY]: {line}")


    async def main(_):
        print("Starting ExampleAPI")
        
        await _.start_comlink()
        
        _.loop = asyncio.get_event_loop()
        _.loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(_.send_stop()))
        _.loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(_.send_stop()))
        
        print("Gathering...")
        await asyncio.gather(
            _.handle_comlink(),
        )

        print("Closing ExampleAPI...")


    async def send_stop(_):
        if _.stopping: return
        _.stopping = True
        
        print("\nStopping ExampleAPI, sending SIGTERM to comlink")
        
        if _.process:
            try: killpg(getpgid(_.process.pid), signal.SIGTERM)
            except ProcessLookupError: pass

            await _.process.wait()
        
        _exit(0)

    

instance = ExampleAPI()
asyncio.run(instance.main())
