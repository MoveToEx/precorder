from multiprocessing import Pipe, Process
from precorder.recorder import run as run_recorder
from logging import getLogger

logger = getLogger(__name__)

def run():
    pc, cc = Pipe()

    recorder = Process(target=run_recorder, args=(pc, ))
    recorder.start()

    logger.info('starting recorder process')

    while True:
        cmd = input()
        if cmd == 's':
            cc.send('start')
            logger.info('start signal sent')
        elif cmd == 't':
            cc.send('stop')
            logger.info('stop signal sent')
        elif cmd == 'i':
            cc.send('inspect')
            logger.info('inspect signal sent')

        elif cmd == 'q':
            cc.send('terminate')
            logger.info('terminate signal sent')
            break
    
    pc.close()