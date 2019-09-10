# @license BSD-3-Clause
#
# Copyright (c) 2019 Quansight. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""TODO"""

import os
import subprocess
from subprocess import CalledProcessError


class Git(object):
    """Class for executing git commands.

    Attributes:
        root: canonical file system path of a git repository
    """

    def __init__(self, root):
        """Initializes a class instance."""
        self.root = os.path.realpath(os.path.expanduser(root))

    def list_current_changed_files(self):
        """Returns the list of files containing changes relative to the index.

        Returns:
            A `dict` containing a list of changed files. If able to successfully resolve a list of changed files, the `dict` has the following format:

            {
                'code': int,          # command status code
                'files': [...string], # list of changed files
                'message': [string]   # error message
            }

            Otherwise, if an error is encountered, the `dict` has the following format:

            {
                'code': int,          # command status code
                'message': [string]   # error message
            }
        """
        cmd = ['git', 'diff', '--name-only']
        response = {}
        try:
            stdout = subprocess.check_output(cmd, cwd=self.root, stderr=subprocess.STDOUT)
            response['files'] = stdout.decode('utf8').strip().split('\n')
            response['code'] = 0
        except CalledProcessError as err:
            response['message'] = err.output.decode('utf8')
            response['code'] = err.returncode

        return response
