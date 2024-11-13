# Copyright (c) 2024
#
# SPDX-License-Identifier: Apache 2.0
from setuptools import setup

setup(
    name='bandit_big_bad_wolf',
    version='0.0.1',
    description='Custom bandit plugin',
    url='None',
    packages=['bandit_big_bad_wolf'],
    author='you',
    install_requires=[
        'bandit',
    ],
    entry_points={
        'bandit.plugins': [
            'os_getcwd = bandit_big_bad_wolf.big_bad_wolf:big_bad_wolf_used',
        ],
    }
)