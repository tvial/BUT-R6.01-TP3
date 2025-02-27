import json
import logging
import os
import sys

import librosa
import numpy as np
from sklearn.decomposition import PCA
import tensorflow as tf
import tensorflow_hub as hub

from models import TrackList


class Embedder:
    def __init__(self):
        logging.info('Create Embedder & load model')
        self.model = hub.load('https://tfhub.dev/google/yamnet/1')

    def process(self, filename):
        logging.info('Read file')
        input_frames, _ = librosa.load(filename, sr=16_000, mono=True, dtype=np.float32)

        # Embed
        logging.info('Compute embedding')
        _, embeddings, _ = self.model(input_frames)

        # Downsample
        logging.info('Downsample')
        n_vectors, n_comps = embeddings.shape
        # Number of vectors per window before down-sampling
        window_size = 10
        n_vectors_in_windows = n_vectors - n_vectors % window_size
        reshaped = tf.reshape(embeddings[:n_vectors_in_windows], (n_vectors // window_size, window_size, n_comps))

        downsampled = tf.math.reduce_mean(reshaped, axis=1)

        # PCA
        logging.info('PCA')
        pca = PCA(n_components=16)
        reduced = pca.fit_transform(downsampled.numpy())

        return reduced


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')

    source_file = sys.argv[1]
    output_dir = sys.argv[2]

    with open(source_file, 'r') as f:
        track_list = TrackList.validate_json(f.read())

    embedder = Embedder()

    for track in track_list:
        output_file = os.path.join(output_dir, f'{track.track_id}.json')
        if os.path.exists(output_file):
            logging.info(f'{track.track_id} - {track.artist} - {track.title}: SKIP')
        else:
            try:
                vectors = embedder.process(track.path)
                entry = {
                    'id': track.track_id,
                    'vectors': [
                        {'vector': list(map(float, vector))}
                        for vector in vectors
                    ]
                }
                with open(output_file, 'w') as f:
                    json.dump(entry, f)
                logging.info(f'{track.track_id} - {track.artist} - {track.title}: CREATE with shape {vectors.shape}')
            except:
                logging.warning(f'{track.track_id} - {track.artist} - {track.title}: ERROR')
