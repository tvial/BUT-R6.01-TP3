import glob
import random
import re

from models import Track, TrackList


ROOT = '/mnt/gargantua/Music'

PARSE_RE = re.compile(rf'^{ROOT}/([^/]+)/([^/]+)/(\d+) - (.+)\.[^.]+$')


def parse_filename(filename):
    m = PARSE_RE.match(filename)
    if m is not None:
        return Track(
            path=filename,
            artist=m.group(1),
            album=m.group(2),
            track_number=int(m.group(3)),
            title=m.group(4)
        )


def validate_entry(track: Track):
    if track is None:
        return False
    if track.album.startswith('_'):
        return False
    if 'various' in track.artist.lower():
        return False
    return True


def dump_cats(track_list, field):
    values = set(getattr(track, field) for track in track_list)
    print()
    print(field)
    print('-' * len(field))
    print('\n'.join(sorted(values)))


if __name__ == '__main__':
    files = glob.glob(ROOT + '/**/*.mp3', recursive=True)
    track_list = list(filter(validate_entry, map(parse_filename, files)))
    random.shuffle(track_list)
    for i, track in enumerate(track_list, 1):
        track.track_id = i

    with open('tracks.json', 'w') as f:
        f.write(TrackList.dump_json(track_list, indent=4).decode('utf8'))
