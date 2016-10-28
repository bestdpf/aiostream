
import pytest
import asyncio
from aiostream import stream, pipe
from aiostream.test_utils import assert_run, event_loop

# Pytest fixtures
assert_run, event_loop


@pytest.mark.asyncio
async def test_just(assert_run):
    value = 3
    xs = stream.just(value)
    await assert_run(xs, [3])


@pytest.mark.asyncio
async def test_throw(assert_run):
    exception = RuntimeError('Oops')
    xs = stream.throw(exception)
    await assert_run(xs, [], exception)


@pytest.mark.asyncio
async def test_empty(assert_run):
    xs = stream.empty()
    await assert_run(xs, [])


@pytest.mark.asyncio
async def test_never(assert_run, event_loop):
    xs = stream.never() | pipe.timeout(30.)
    await assert_run(xs, [], asyncio.TimeoutError())
    assert event_loop.steps == [30.]


@pytest.mark.asyncio
async def test_range(assert_run, event_loop):
    xs = stream.range(3, 10, 2, interval=1.0)
    await assert_run(xs, [3, 5, 7, 9])
    assert event_loop.steps == [1, 1, 1]


@pytest.mark.asyncio
async def test_count(assert_run):
    xs = stream.count(3, 2)[:4]
    await assert_run(xs, [3, 5, 7, 9])


@pytest.mark.asyncio
async def test_iterable(assert_run):
    lst = [9, 4, 8, 3, 1]

    xs = stream.from_iterable(lst)
    await assert_run(xs, lst)

    xs = stream.iterate(lst)
    await assert_run(xs, lst)


@pytest.mark.asyncio
async def test_aiterable(assert_run, event_loop):

    async def agen():
        for x in range(2, 5):
            yield await asyncio.sleep(1.0, result=x**2)

    xs = stream.from_aiterable(agen())
    await assert_run(xs, [4, 9, 16])
    assert event_loop.steps == [1.0, 1.0, 1.0]

    xs = stream.iterate(agen())
    await assert_run(xs, [4, 9, 16])
    assert event_loop.steps == [1.0, 1.0, 1.0]*2


@pytest.mark.asyncio
async def test_non_iterable(assert_run):
    exception = TypeError('Not (async) iterable',)
    xs = stream.iterate(None)
    await assert_run(xs, [], exception)
