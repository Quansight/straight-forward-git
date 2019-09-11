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

"""Execute Git commands."""

import os
import subprocess
import tornado.web

# Please keep class methods ordered in alphabetical order...


class Git():
    """Class for executing Git commands.

    Attributes:
        root: canonical file system path of a Git repository

    """

    def __init__(self, root):
        """Initialize a class instance."""
        self.root = os.path.realpath(os.path.expanduser(root))

    def add(self, path='.', update_all=True):
        """Add file contents to the index.

        Args:
            path: a subdirectory path, file path, glob, or a list of paths and/or globs (default: '.')
            update_all: boolean indicating whether to update all entries in the index to match the working tree (default: True)

        Returns:
            A `dict` containing command results. If able to successfully execute command, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        """
        cmd = ['git', 'add']
        if update_all:
            cmd.append('-A')

        if isinstance(path, str):
            cmd.append(path)
        else:
            # Assume we have been provided a list:
            cmd = cmd + path

        response = {}
        try:
            stdout = subprocess.run(cmd, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            response['code'] = err.returncode
            response['message'] = err.output.decode('utf8')
            return response

        response['code'] = 0
        response['message'] = stdout.decode('utf8').strip()

        return response

    def checkout_branch(self, branch):
        """Switch to a specified branch.

        Notes:
            If a specified branch does not exist, the branch is created.

        Args:
            branch: branch name

        Returns:
            A `dict` containing command results. If able to successfully execute command, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        Raises:
            HTTPError: must provide a branch argument

        """
        if not isinstance(branch, str):
            raise tornado.web.HTTPError(400, 'invalid argument. Must provide a valid branch argument.')

        cmd1 = ['git', 'show-ref', '--quiet', 'refs/heads/'+branch]
        cmd2 = ['git', 'checkout']
        try:
            stdout = subprocess.run(cmd1, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            cmd2.append('-b')

        cmd2.append(branch)
        response = {}
        try:
            stdout = subprocess.run(cmd2, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            response['code'] = err.returncode
            response['message'] = err.output.decode('utf8')
            return response

        response['code'] = 0
        response['message'] = stdout.decode('utf8').strip()

        return response

    def commit_history(self, path='.', n=None):
        """Return a commit history.

        Args:
            path: subdirectory path (default: '.')
            n: number of commits

        Returns:
            A `dict` containing the commit history. If able to successfully resolve a commit history, the returned `dict` has the following format:

            {
                'code': int,              # command status code
                'history': [...dict]      # commits
            }

            Each `dict` in `history` has the following format:

            {
                'hash': string,           # commit hash
                'author': string,         # commit author
                'relative_date': string,  # relative date of commit
                'message': string         # commit message
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        """
        cmd = ['git', 'log', '--pretty=format:%H%n%an%n%ar%n%s']
        if n is not None:
            cmd.append('-n '+str(n))
        cmd.append(path)

        response = {}
        try:
            stdout = subprocess.run(cmd, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            response['code'] = err.returncode
            response['message'] = err.output.decode('utf8')
            return response

        response['code'] = 0
        lines = stdout.decode('utf8').strip()
        if lines == '':
            response['history'] = []
        else:
            response['history'] = []
            stride = 4
            i = 0
            lines = lines.split('\n')
            while i < len(lines):
                tmp = {}
                tmp['hash'] = lines[i]
                tmp['author'] = lines[i+1]
                tmp['relative_date'] = lines[i+2]
                tmp['message'] = lines[i+3]
                response['history'].append(tmp)
                i += stride

        return response

    def current_branch(self):
        """Return the current branch.

        Returns:
            A `dict` containing the current branch. If able to successfully resolve the current branch, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'branch': string      # branch name
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        """
        cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
        response = {}
        try:
            stdout = subprocess.run(cmd, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            response['code'] = err.returncode
            response['message'] = err.output.decode('utf8')
            return response

        response['code'] = 0
        response['branch'] = stdout.decode('utf8').strip()

        return response

    def delete_branch(self, branch, force=False):
        """Delete a specified branch.

        Args:
            branch: branch name
            force: boolean indicating whether to force delete a specified branch (default: False)

        Returns:
            A `dict` containing command results. If able to successfully execute command, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        Raises:
            HTTPError: must provide a branch argument

        """
        if not isinstance(branch, str):
            raise tornado.web.HTTPError(400, 'invalid argument. Must provide a valid branch argument.')

        cmd = ['git', 'branch', '-d']
        if force:
            cmd.append('-f')
        cmd.append(branch)

        response = {}
        try:
            stdout = subprocess.run(cmd, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            response['code'] = err.returncode
            response['message'] = err.output.decode('utf8')
            return response

        response['code'] = 0
        response['message'] = stdout.decode('utf8').strip()

        return response

    def init(self):
        """Create an empty Git repository or reinitialize an existing repository.

        Returns:
            A `dict` containing command results. If able to successfully execute command, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        """
        cmd = ['git', 'init']
        response = {}
        try:
            stdout = subprocess.run(cmd, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            response['code'] = err.returncode
            response['message'] = err.output.decode('utf8')
            return response

        response['code'] = 0
        response['message'] = stdout.decode('utf8').strip()

        return response

    def list_current_changed_files(self, path='.'):
        """Return the list of files containing changes relative to the index.

        Args:
            path: subdirectory path (default: '.')

        Returns:
            A `dict` containing a list of changed files. If able to successfully resolve a list of changed files, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'files': [...string]  # list of changed files
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        """
        cmd = ['git', 'diff', '--name-only', path]
        response = {}
        try:
            stdout = subprocess.run(cmd, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            response['code'] = err.returncode
            response['message'] = err.output.decode('utf8')
            return response

        response['code'] = 0
        lines = stdout.decode('utf8').strip()
        if lines == '':
            response['files'] = []
        else:
            response['files'] = lines.split('\n')

        return response

    def reset(self, path=None):
        """Remove file contents from the index.

        Notes:
            If not provided a path, this method removes all file contents from the index.

        Args:
            path: a subdirectory path, file path, glob, or a list of paths and/or globs

        Returns:
            A `dict` containing command results. If able to successfully execute command, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        """
        cmd = ['git', 'reset']
        if path is not None:
            if isinstance(path, str):
                cmd.append(path)
            else:
                # Assume we have been provided a list:
                cmd = cmd + path

        response = {}
        try:
            stdout = subprocess.run(cmd, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            response['code'] = err.returncode
            response['message'] = err.output.decode('utf8')
            return response

        response['code'] = 0
        response['message'] = stdout.decode('utf8').strip()

        return response

    def run(self, args='help'):
        """Run a Git command.

        Args:
            args: Git command arguments (default: 'help')

        Returns:
            A `dict` containing the command results. If able to successfully execute a command, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'results': string     # command results
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        """
        cmd = ['git']
        if isinstance(args, str):
            cmd.append(args)
        else:
            cmd = cmd + args

        response = {}
        try:
            stdout = subprocess.run(cmd, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            response['code'] = err.returncode
            response['message'] = err.output.decode('utf8')
            return response

        response['code'] = 0
        response['results'] = stdout.decode('utf8').strip()

        return response

    def status(self, path='.'):
        """Return the working tree status.

        Args:
            path: subdirectory path (default: '.')

        Returns:
            A `dict` containing a list of changes. If able to successfully resolve a list of changes, the returned `dict` has the following format:

            {
                'code': int,              # command status code
                'differences': [...dict]  # list of changes
            }

            For modifications, additions, and deletions, each `dict` in `differences` has the following format:

            {
                'status': string,  # single-letter action abbreviation
                'action': string,  # action
                'file': string     # changed file
            }

            For copies and renames, each `dict` in `differences` has the following format:

            {
                'status': string,  # single-letter action abbreviation
                'action': string,  # action
                'to': string,      # original path
                'from': string     # destination path
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        """
        cmd = ['git', 'status', '--porcelain', '--renames', path]
        response = {}
        try:
            stdout = subprocess.run(cmd, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            response['code'] = err.returncode
            response['message'] = err.output.decode('utf8')
            return response

        response['code'] = 0
        response['differences'] = []
        lines = stdout.decode('utf8').strip()
        if lines == '':
            return response

        lines = lines.split('\n')
        for line in lines:
            line = line.strip()
            tmp = {}
            tmp['status'] = line[0]
            if line[0] == 'M':
                tmp['action'] = 'modified'
                tmp['file'] = line[2:]
            elif line[0] == 'A':
                tmp['action'] = 'added'
                tmp['file'] = line[2:]
            elif line[0] == 'D':
                tmp['action'] = 'deleted'
                tmp['file'] = line[2:]
            elif line[0] == 'C':
                line = line[2:].split(' -> ')
                tmp['action'] = 'copied'
                tmp['from'] = line[0]
                tmp['to'] = line[1]
            elif line[0] == 'R':
                line = line[2:].split(' -> ')
                tmp['action'] = 'renamed'
                tmp['from'] = line[0]
                tmp['to'] = line[1]
            elif line[0] == '?':
                tmp['action'] = 'untracked'
                tmp['file'] = line[3:]
            response['differences'].append(tmp)

        return response
