import aiostream.stream.create as s_create
import asyncio


class StreamIterator(object):

    def __init__(self):
        self._future = asyncio.Future()

    def __aiter__(self):
        return self

    async def __anext__(self):
        await self._future
        print('1here')
        ret = self._future.result()
        self._future = asyncio.Future()
        return ret

    async def append(self, ret):
        self._future.set_result(ret)
        print('here')
        await asyncio.sleep(0)
        print('here')
        #self._future.done()
        #self._future = asyncio.Future()

    async def read(self):
        return await self._future

    async def aclose(self):

        self._future = None

async def get_iter(it):
    print ('get_iter')
    async for item in it:
        print(item)


async def put_iter(it):
    i = 0
    while True:
        await asyncio.sleep(3)
        i += 1
        print('before append')
        await it.append(i)
        #await asyncio.sleep(1)

if __name__ == '__main__':
    it = StreamIterator()
    # it = s_create.iterate(it)
    task2 = asyncio.get_event_loop().create_task(put_iter(it))
    task1 = asyncio.get_event_loop().create_task(get_iter(it))
    asyncio.get_event_loop().run_forever()

