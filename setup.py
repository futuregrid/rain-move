# -------------------------------------------------------------------------- #
# Copyright 2010-2011, Indiana University                                    #
#                                                                            #
# Licensed under the Apache License, Version 2.0 (the "License"); you may    #
# not use this file except in compliance with the License. You may obtain    #
# a copy of the License at                                                   #
#                                                                            #
# http://www.apache.org/licenses/LICENSE-2.0                                 #
#                                                                            #
# Unless required by applicable law or agreed to in writing, software        #
# distributed under the License is distributed on an "AS IS" BASIS,          #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
# See the License for the specific language governing permissions and        #
# limitations under the License.                                             #
# -------------------------------------------------------------------------- #

from distribute_setup import use_setuptools
use_setuptools(version="0.6.15")
from setuptools import setup, find_packages
import sys
sys.path.insert(0, './src')
from futuregrid_move import RELEASE

setup(
    name = 'futuregrid_move',
    version = RELEASE,
    description = "FutureGrid Rain Move is a software to move resources between infrastructures. This will be part of Rain.",
    author = 'Javier Diaz, Fugang Wang, Koji Tanaka, Gregor von Laszewski',
    author_email = 'javier.diazmontes@gmail.com',
    license = "Apache Software License",
    url = "http://futuregrid.github.com/rain_move/index.html",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Distributed Computing"
        ],
    keywords = "Cloud, Grid, HPC",
    package_dir = {'': 'src'},
    packages = find_packages("src"),
    data_files = [
        ('/etc/futuregrid', ['etc/fg-server.conf-sample_move', 'etc/fg-client.conf-sample_move'])
        ],
    scripts = [
        'src/futuregrid_move/rain/move/RainMoveServer.py',
        'src/futuregrid_move/rain/move/RainMoveServerSites.py',
        'src/futuregrid_move/rain/move/fg-move',
        ],
    install_requires = ['setuptools', 'cmd2','argparse', 'python-ldap'],
    zip_safe = False,
    include_package_date=True
    )

