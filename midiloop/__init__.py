#!/usr/bin/env python3

import argparse
import logging
import mido
import time

logger = logging.getLogger('midiloop')

def pluralize(s: str, value: int) -> str:
    return s if value == 1 else f'{s}s'

def run_midi_device(name: str):
    with mido.open_input(name, virtual=True) as inp:
        with mido.open_output(name, virtual=True) as out:
            logger.info("Opened MIDI device '%s'", name)

            last = time.time()
            mps = 0

            for message in inp:
                out.send(message)
                logger.debug('%s', message)
                mps += 1

                now = time.time()
                if now - last >= 1:
                    logger.info('%d %s/second', mps, pluralize('message', mps))
                    last = now
                    mps = 0

def main():
    parser = argparse.ArgumentParser(description='Creates a virtual loopback MIDI device')
    parser.add_argument('-n', '--name', default='Loop', help='The name of the virtual MIDI device')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging of messages')

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)-6s %(message)s')
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    try:
        run_midi_device(name=args.name)
    except KeyboardInterrupt:
        logger.info('Closing')
