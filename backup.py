import yaml
import subprocess
import argparse
import os

def get_volume_names():
    with open('docker-compose.yaml', 'r') as f:
        d = yaml.load(f, Loader=yaml.BaseLoader)
        return list(d['volumes'].keys())

def get_existing_volumes():
    return set(map(lambda b: b.decode('utf-8'), subprocess.check_output(['docker', 'volume', 'list', '-q']).split()))

parser = argparse.ArgumentParser()

subparser = parser.add_subparsers(dest='command')
backup_parser = subparser.add_parser('backup')
restore_parser = subparser.add_parser('restore')
restore_parser.add_argument('-f', '--force', action='store_true')

args = parser.parse_args()

print(args)
existing_volumes = get_existing_volumes()
if args.command == 'backup':
    for volume in get_volume_names():
        print('Backing up volume {}'.format(volume))
        if volume not in existing_volumes:
            print('WARNING: Volume {} does not exist. Skipping.'.format(volume))
            continue
        subprocess.check_call(['docker', 'run', '--rm', '-v', '{}:/data'.format(volume), '-v', '{}:/backup'.format(os.getcwd()), 'busybox', 'tar', 'cvf', '/backup/{}.tar'.format(volume), '/data/'])
else:
    pass
#subprocess.check_call(['docker', 'run', '--rm', '-v', '{}:/data'.format(volume), '-v', '{}:/backup'.format(os.getcwd()), 'busybox', 'tar', 'xvf', '/backup/{}.tar'.format(volume)'])
