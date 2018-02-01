#!/usr/bin/env python
"""
ENV variables
- mujoco_key_text: plain text environment value
- repo_surreal: /mylibs/surreal/surreal
- repo_tensorplex

"""
import os
import sys
import argparse
import shutil
import glob
import errno

parser = argparse.ArgumentParser()
parser.add_argument('--cmd', type=str, nargs='+', help='run arbitrary command')
parser.add_argument('--sh', type=str, default='', help='shell script')
parser.add_argument('--bash', action='store_true', help='start interactive bash')
parser.add_argument('--py', type=str, default='', help='python script')

args = parser.parse_args()


def f_copy(fsrc, fdst):
    """
    If exist, remove. Supports both dir and file. Supports glob wildcard.
    """
    for f in glob.glob(fsrc):
        try:
            shutil.copytree(f, fdst)
        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy(f, fdst)


def init():
    os.system('/usr/bin/Xorg -noreset +extension GLX '
              '+extension RANDR +extension RENDER -logfile /etc/fakeX/10.log '
              '-config /etc/fakeX/xorg.conf :10 > /dev/null 2>&1 &')
    mujoco_key = os.environ.get('mujoco_key_text', '')
    if mujoco_key:
        with open('/root/.mujoco/mjkey.txt', 'w') as fp:
            fp.write(mujoco_key)
    else:
        print('WARNING: missing Mujoco `mjkey.txt`')

    surreal_path = os.environ.get('repo_surreal', '')
    if surreal_path and os.path.exists(surreal_path):
        # pip install surreal will move to Dockerfile if we release the image
        # here is only for dev, surreal is reinstalled every time
        os.system('pip install -e ' + surreal_path)
    else:
        print('WARNING: `surreal` lib not installed')
    tensorplex_path = os.environ.get('repo_tensorplex', '')
    if tensorplex_path and os.path.exists(tensorplex_path):
        os.system('pip install -e ' + tensorplex_path)
    else:
        print('WARNING: `tensorplex` lib not installed')


init()


if args.bash:
    os.system('bash')
elif args.cmd:
    os.system(' '.join(args.cmd))
elif args.py:
    assert args.py.endswith('.py')
    os.system('python -u ' + args.py)
elif args.sh:
    os.system('/bin/bash ' + args.bash)
else:
    print('No args given to /mylibs/entry.py')
