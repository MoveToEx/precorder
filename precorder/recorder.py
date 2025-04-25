from multiprocessing.connection import PipeConnection
from pyaudio import PyAudio, paInt16
from pathlib import Path
from logging import getLogger
from wave import open as wvopen, Wave_write
from collections import deque
from time import time

logger = getLogger(__name__)

OUTDIR = Path('./output')

OUTFILE = OUTDIR / f'record-{time():.0f}.wav'

SAMPLE_RATE = 44100
FORMAT = paInt16
CHANNELS = 2
CHUNK_SIZE = 1024
BUF_SIZE = 1024
DEVICE = 1

if not OUTDIR.exists():
    OUTDIR.mkdir()

def run(pipe: PipeConnection):
    queue = deque[bytes](maxlen=BUF_SIZE)
    pa = PyAudio()
    stream = pa.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True)

    logger.info(f'using device {pa.get_device_info_by_index(DEVICE)['name']}')
    logger.info(f'recording with {CHANNELS} ch, {SAMPLE_RATE / 1000} KHz @ {pa.get_sample_size(FORMAT) * SAMPLE_RATE * CHANNELS * 8 / 1024:.2f} Kbps')
    logger.info(f'buffer size = {BUF_SIZE * CHUNK_SIZE * CHANNELS * pa.get_sample_size(FORMAT) / 1024 / 1024:.2f} MiB')
    logger.info(f'estimated buffer duration = {BUF_SIZE * CHUNK_SIZE / SAMPLE_RATE:.2f}s')

    wavefile: Wave_write | None = None

    while True:
        if pipe.poll():
            cmd: str = pipe.recv()

            if cmd == 'start':
                if wavefile is not None:
                    logger.warning('already recording')
                    continue

                logger.info('starting record')

                filename = str(OUTDIR / f'record-{time():.0f}.wav')

                logger.info('flushing ' + str(len(queue)) + ' chunks')

                wavefile = wvopen(filename, 'wb')
                wavefile.setparams((CHANNELS, pa.get_sample_size(FORMAT), SAMPLE_RATE, 0, 'NONE', 'NONE'))

                while len(queue):
                    wavefile.writeframes(queue.popleft())

                logger.info('-> ' + filename)
            elif cmd == 'stop':
                if wavefile is None:
                    logger.warning('not recording')
                    continue

                logger.info('stopping record')

                logger.info('closing wave output')
                wavefile.close()
                wavefile = None
                
            elif cmd == 'terminate':
                logger.info('terminating')
                break
            elif cmd == 'inspect':
                logger.info(f'state = {'not ' if wavefile is None else ''}recording')
                logger.info(f'queue size = {len(queue)}')
                logger.info(f'queue duration = {len(queue) * CHUNK_SIZE / SAMPLE_RATE:.2f}s')
                if wavefile:
                    logger.info(f'output file offset = {wavefile.tell()}')

        chunk = stream.read(CHUNK_SIZE)

        if wavefile is not None:
            wavefile.writeframes(chunk)
        else:
            queue.append(chunk)

    stream.close()
    if wavefile is not None:
        logger.info('closing wave output')
        wavefile.close()
    pipe.close()
    pa.terminate()

