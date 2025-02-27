import itertools as it
import logging
import os
import random
import sys

from models import TrackList


def make_metadata(track_list, output_dir):
    metadata_file = os.path.join(output_dir, 'metadata.csv')
    with open(metadata_file, 'w') as f:
        f.write('song_id;artist;title;duration\n')
        for track in track_list:
            duration = random.randint(120, 600)
            f.write(f'{track.track_id};{track.artist};{track.title};{duration}\n')


def batched(iterable, n):
    iterator = iter(iterable)
    while batch := tuple(it.islice(iterator, n)):
        yield batch


def compact_vectors(track_list, vectors_dir, output_dir, n_per_file):
    for i, batch in enumerate(batched(track_list, n_per_file), 1):
        file_name = os.path.join(output_dir, f'vectors_{i:03}.jsonl')
        logging.info('Batch %s', file_name)
        with open(file_name, 'wb') as output:
            for track in batch:
                track_file = os.path.join(vectors_dir, f'{track.track_id}.json')
                if os.path.exists(track_file):
                    with open(track_file, 'rb') as input:
                        output.write(input.read() + b'\n')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')

    tracks_file = sys.argv[1]
    vectors_dir = sys.argv[2]
    output_dir = sys.argv[3]

    with open(tracks_file, 'r') as f:
        track_list = TrackList.validate_json(f.read())

    make_metadata(track_list, output_dir)
    compact_vectors(track_list, vectors_dir, output_dir, 80)
