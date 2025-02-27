import json
import logging
import os
import random
import sys


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')

    track_ids = map(int, sys.argv[1].split(','))
    output_dir = sys.argv[2]

    output_file = os.path.join(output_dir, 'queries.jsonl')
    with open(output_file, 'w') as f:
        for i, track_id in enumerate(track_ids, 1):
            logging.info('Nudge %s', track_id)
            vector_file = os.path.join('output', f'{track_id}.json')
            with open(vector_file, 'r') as g:
                entry = json.load(g)
            for vector in entry['vectors']:
                vector['vector'] = [x * (.95 + .1*random.random()) for x in vector['vector']]
            entry['id'] = i
            f.write(json.dumps(entry) + '\n')
