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

    def _run(self, cmd, clbk=None):
        """Execute a Git command.

        Notes:
            When a Git command successfully executes, a provided callback function is provided two arguments:

                -   response: output response `dict`
                -   raw: string containing raw command results

            The response `dict` provided to the callback function can be extended and has the following format:

            {
                'code': int           # command status code
            }

            Otherwise, if not provided a callback function, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # raw command results
            }

            If an error occurs during command execution, the provided callback is not invoked and the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        Args:
            cmd: command to run
            clbk: function which processes command results upon successful command execution

        Returns:
            A `dict` containing command results.

        """
        response = {}
        try:
            stdout = subprocess.run(cmd, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError as err:
            response['code'] = err.returncode
            response['message'] = err.output.decode('utf8')
            return response

        response['code'] = 0
        if clbk is not None:
            clbk(response, stdout.decode('utf8').strip())
        else:
            response['message'] = stdout.decode('utf8').strip()

        return response

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

        return self._run(cmd)

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
            subprocess.run(cmd1, cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
        except subprocess.CalledProcessError:
            cmd2.append('-b')

        cmd2.append(branch)
        return self._run(cmd2)

    def commit(self, subject, body=None):
        """Record changes to the repository.

        Args:
            subject: commit subject/summary
            body: commit description

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
            HTTPError: must provide a valid subject argument

        """
        if not isinstance(subject, str) or subject == '':
            raise tornado.web.HTTPError(400, 'invalid argument. Must provide a valid subject argument.')

        cmd = ['git', 'commit', '-m', subject]
        if body is not None:
            cmd.append('-m')
            cmd.append(body)

        return self._run(cmd)

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
        def clbk(response, lines):
            """Process command results.

            Args:
                response: response `dict`
                lines: command results

            """
            response['history'] = []
            if lines == '':
                return

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

        cmd = ['git', 'log', '--pretty=format:%H%n%an%n%ar%n%s']
        if n is not None:
            cmd.append('-n '+str(n))
        cmd.append(path)
        return self._run(cmd, clbk)

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
        def clbk(response, branch):
            """Process command results.

            Args:
                response: response `dict`
                branch: branch name

            """
            response['branch'] = branch

        cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
        return self._run(cmd, clbk)

    def current_changed_files(self, path='.'):
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
        def clbk(response, lines):
            """Process command results.

            Args:
                response: response `dict`
                lines: command results

            """
            if lines == '':
                response['files'] = []
            else:
                response['files'] = lines.split('\n')

        cmd = ['git', 'diff', '--name-only', path]
        return self._run(cmd, clbk)

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
        return self._run(cmd)

    def delete_untracked_files(self, path='.'):
        """Delete untracked files.

        Args:
            path: subdirectory path (default: '.')

        Returns:
            A `dict` containing command results. If able to successfully delete untracked files, the returned `dict` has the following format:

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
        cmd = ['git', 'clean', '-df', path]
        return self._run(cmd)

    def fetch(self, remote=None, prune=False, fetch_all=False):
        """Download objects and refs from a remote repository.

        Args:
            remote: name of remote (default: 'origin')
            prune: boolean indicating whether to remove any remote-tracking references that no longer exist on the remote
            fetch_all: boolean indicating whether to fetch all remotes

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
        cmd = ['git', 'fetch']
        if prune:
            cmd.append('--prune')
        if fetch_all:
            cmd.append('--all')
        if remote is not None:
            cmd.append(remote)

        return self._run(cmd)

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
        return self._run(cmd)

    def local_branches(self):
        """Return a list of local branches.

        Returns:
            A `dict` containing a list of local branches. If able to successfully resolve a list of local branches, the returned `dict` has the following format:

            {
                'code': int,             # command status code
                'branches': [...string]  # list of branches
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,             # command status code
                'message': string        # error message
            }

        """
        def clbk(response, lines):
            """Process command results.

            Args:
                response: response `dict`
                lines: command results

            """
            if lines == '':
                response['branches'] = []
            else:
                response['branches'] = lines.split('\n')

        cmd = ['git', 'for-each-ref', '--format=\'%(refname:short)\'', 'refs/heads/']
        return self._run(cmd, clbk)

    def push(self, remote, branch=None):
        """Update remote refs along with associated objects.

        Args:
            remote: remote name
            branch: branch name (default: current branch name)

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
        if not isinstance(remote, str):
            raise tornado.web.HTTPError(400, 'invalid argument. Must provide a valid remote argument.')

        cmd = ['git', 'push', remote]
        if branch is None:
            cmd.append(self.current_branch()['branch'])
        else:
            cmd.append(branch)

        return self._run(cmd)

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

        return self._run(cmd)

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
        def clbk(response, results):
            """Process command results.

            Args:
                response: response `dict`
                results: command results

            """
            response['results'] = results

        cmd = ['git']
        if isinstance(args, str):
            cmd.append(args)
        else:
            cmd = cmd + args

        return self._run(cmd, clbk)

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
        def clbk(response, lines):
            """Process command results.

            Args:
                response: response `dict`
                lines: command results

            """
            response['differences'] = []
            if lines == '':
                return

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

        cmd = ['git', 'status', '--porcelain', '--renames', path]
        return self._run(cmd, clbk)

    def untracked_files(self, path='.'):
        """Return the list of untracked files.

        Args:
            path: subdirectory path (default: '.')

        Returns:
            A `dict` containing a list of untracked files. If able to successfully resolve a list of untracked files, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'files': [...string]  # list of untracked files
            }

            Otherwise, if an error is encountered, the returned `dict` has the following format:

            {
                'code': int,          # command status code
                'message': string     # error message
            }

        """
        def clbk(response, lines):
            """Process command results.

            Args:
                response: response `dict`
                lines: command results

            """
            if lines == '':
                response['files'] = []
            else:
                response['files'] = lines.split('\n')

        cmd = ['git', 'ls-files', '-o', '--exclude-standard', path]
        return self._run(cmd, clbk)
