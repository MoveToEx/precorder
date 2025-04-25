from multiprocessing import Pipe, Process
from precorder.recorder import run as run_recorder
from logging import getLogger

logger = getLogger(__name__)

SIGNALS = {
    's': 'start',
    't': 'stop',
    'i': 'inspect',
    'q': 'terminate',
    'f': 'flush',
    'c': 'clear'
}

def run():
    pc, cc = Pipe()

    recorder = Process(target=run_recorder, args=(pc, ))
    recorder.start()

    logger.info('starting recorder process')

    while True:
        cmd = input()

        if cmd not in SIGNALS:
            logger.warning('unknown command ' + cmd)
            continue

        cc.send(SIGNALS[cmd])
        logger.info('send ' + SIGNALS[cmd])

        if cmd == 'q':
            break
    
    pc.close()