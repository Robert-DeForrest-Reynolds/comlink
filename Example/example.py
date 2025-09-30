from sys import stdin, stdout, stderr, exit
from os import path, getcwd, _exit, mkdir
import asyncio, signal
from asyncio.subprocess import PIPE, Process
from typing import Callable


class ExampleAPI:
    process: Process
    event_loop: asyncio.AbstractEventLoop
    commands:dict[str:Callable]

    def __init__(_):
        _.stopping = False
        _.commands = {
            'init': _.initialize_comlink,
            'close': lambda: asyncio.create_task(_.send_stop()),
        }


    def initialize_comlink(_):
        if not path.exists('comlink'):
            print('Creating comlink directory')
            mkdir('comlink')
        else:
            print("comlink already initialized; comlink directory already exists")


    async def start_comlink(_):
        _.process = await asyncio.create_subprocess_exec(
            'python', '-u', path.join('..', 'comlink', '__main__.py'), getcwd(),
            stdin=PIPE, stdout=PIPE, stderr=PIPE,
        )
        await asyncio.sleep(0.1)
        if _.process.returncode is not None:
            err = await _.process.stderr.read()
            print("Process failed:", err.decode())
            await _.send_stop()


    async def pump_stdin(_):
        loop = asyncio.get_event_loop()
        while not _.stopping:
            line = await loop.run_in_executor(None, stdin.readline)
            if not line: continue
            if _.process.stdin.is_closing(): break
            if line[0] == '>':
                _.commands[line[1:-1] if line[-1] == '\n' else line[1:]]()
            else:
                _.process.stdin.write((line + "\n").encode())
            await _.process.stdin.drain()


    async def pump_stdout(_):
        while not _.stopping:
            line = await _.process.stdout.readline()
            if not line: break
            if line == '' or line == '\n': continue
            text = line.decode()
            if text.startswith("~"):
                print(f"[OUTPUT]: {text.strip()}")
            else:
                print(f"[REPLY]: {text.strip()}")


    async def pump_stderr(_):
        while not _.stopping:
            line = await _.process.stderr.readline()
            if not line: break
            if line == '' or line == '\n': continue
            print(f"[DEBUG]: {line.decode().strip()}")


    async def send_stop(_):
        if _.stopping:
            return
        _.stopping = True

        print("\nStopping ExampleAPI, sending SIGTERM to comlink...")

        for t in _.tasks:
            if t._coro.__name__ == 'pump_stdin':
                t.cancel()

        if _.process:
            try:
                _.process.stdin.write(b'!\n')
                await _.process.stdin.drain()
                _.process.stdin.close()

                # drain stdout/stderr until process exits
                await asyncio.gather(_.pump_stdout(), _.pump_stderr())
                await _.process.wait()
            except Exception as e:
                print("Error sending stop:", e)

        print("Closing...")
        exit(0)


    async def main(_):
        print("Starting ExampleAPI")

        await _.start_comlink()

        _.loop = asyncio.get_event_loop()

        signal.signal(signal.SIGINT, lambda s, f: asyncio.create_task(_.send_stop()))

        print("Gathering...")
        _.tasks = [
            asyncio.create_task(_.pump_stdin()),
            asyncio.create_task(_.pump_stdout()),
            asyncio.create_task(_.pump_stderr()),
        ]
        await asyncio.gather(*_.tasks, return_exceptions=True)

        print("Closing ExampleAPI...")
        return


instance = ExampleAPI()
asyncio.run(instance.main())
