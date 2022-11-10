import asyncio
import aconsole

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    console = AsyncConsole()
    console.title('echo test')

    async def echo():
        while True:
            result = await console.input('echo to out: ')
            console.print('echo:', result)

    run_task = console.run(loop)
    loop.create_task(echo())
    loop.run_until_complete(run_task) # wait until window closed