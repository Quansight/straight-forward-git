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

"""Individual handlers which execute Git commands and return results to the frontend."""

# pylint: disable=W0223

import tornado.web
from notebook.base.handlers import APIHandler
from notebook.utils import url_path_join


class BaseHandler(APIHandler):
    """Base handler class.

    Attributes:
        git: Git command executer

    """

    @property
    def git(self):
        """Return the Git command executor."""
        return self.settings['git']


# Please keep handler classes in alphabetical order...

class AddFiles(BaseHandler):
    """Handler for adding file contents to the index."""

    def post(self):
        """Add file contents to the index.

        Fields:
            path: a subdirectory path, file path, glob, or a list of paths and/or globs (optional)
            update_all: boolean indicating whether to update all entries in the index to match the working tree (optional)

        Response:
            A JSON object having the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

        """
        data = self.get_json_body()
        if 'path' in data:
            path = data['path']
        else:
            path = '.'

        if 'update_all' in data and data['update_all'] == 'False':
            update_all = False
        else:
            update_all = True

        res = self.git.add(path, update_all)
        self.finish(res)


class CheckoutBranch(BaseHandler):
    """Handler for switching to a specified branch."""

    def post(self):
        """Switch to a specified branch.

        Fields:
            branch: branch name

        Response:
            A JSON object having the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

        """
        data = self.get_json_body()
        if 'branch' not in data:
            raise tornado.web.HTTPError(400, 'must provide a branch name')

        res = self.git.checkout_branch(data['branch'])
        self.finish(res)


class Commit(BaseHandler):
    """Handler to record changes to the repository."""

    def post(self):
        """Record changes to the repository.

        Fields:
            subject: commit subject/summary
            body: commit description (optional)

        Response:
            A JSON object having the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

        """
        data = self.get_json_body()
        if 'subject' not in data:
            raise tornado.web.HTTPError(400, 'must provide a subject')

        if 'body' in data:
            body = data['body']
        else:
            body = None

        res = self.git.commit(data['subject'], body)
        self.finish(res)


class CommitHistory(BaseHandler):
    """Handler for returning a commit history."""

    def get(self):
        """Return a commit history.

        Fields:
            path: subdirectory path (optional)
            n: number of commits (optional)

        Response:
            A JSON object having the following format:

            {
                'code': int,               # command status code
                'history': [...Object]     # command results
            }

            where each `Object` in `history` has the following format:


            {
                'hash': string,           # commit hash
                'author': string,         # commit author
                'relative_date': string,  # relative date of commit
                'message': string         # commit message
            }

        """
        path = self.get_query_argument('path', default='.')
        n = self.get_query_argument('n', default=None)
        res = self.git.commit_history(path, n)
        self.finish(res)


class CurrentBranch(BaseHandler):
    """Handler for returning the current branch."""

    def get(self):
        """Return the current branch.

        Response:
            A JSON object having the following format:

            {
                'code': int,          # command status code
                'branch': string      # branch name
            }

        """
        res = self.git.current_branch()
        self.finish(res)


class CurrentChangedFiles(BaseHandler):
    """Handler for retrieving the list of files containing changes relative to the index."""

    def get(self):
        """Retrieve the list of files containing changes relative to the index.

        Response:
            A JSON object having the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

        """
        path = self.get_query_argument('path', default='.')
        res = self.git.current_changed_files(path)
        self.finish(res)


class DeleteBranch(BaseHandler):
    """Handler to delete a specified branch."""

    def delete(self):
        """Delete a specified branch.

        Fields:
            branch: branch name
            force: boolean indicating whether to force delete a specified branch (optional)

        Response:
            A JSON object having the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

        """
        branch = self.get_query_argument('branch')
        force = self.get_query_argument('force', default='False')
        if force == 'True':
            force = True
        elif force == 'False':
            force = False

        self.git.delete_branch(branch, force)


class DeleteUntrackedFiles(BaseHandler):
    """Handler for deleting untracked files."""

    def delete(self):
        """Delete untracked files.

        Fields:
            path: subdirectory path (optional)

        Response:
            A JSON object having the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

        """
        path = self.get_query_argument('path', default='.')
        res = self.git.delete_untracked_files(path)
        self.finish(res)


class Fetch(BaseHandler):
    """Handler to download objects and refs from a remote repository."""

    def get(self):
        """Download objects and refs from a remote repository.

        Fields:
            remote: name of remote (optional)
            prune: boolean indicating whether to remove any remote-tracking references that no longer exist on the remote (optional)
            fetch_all: boolean indicating whether to fetch all remotes (optional)

        Response:
            {
                'code': int,          # command status code
                'message': string     # command results
            }

        """
        remote = self.get_query_argument('remote', default=None)
        prune = self.get_query_argument('prune', default='False')
        if prune == 'True':
            prune = True
        elif prune == 'False':
            prune = False

        fetch_all = self.get_query_argument('fetch_all', default='False')
        if fetch_all == 'True':
            fetch_all = True
        elif fetch_all == 'False':
            fetch_all = False

        res = self.git.fetch(remote, prune, fetch_all)
        self.finish(res)


class Init(BaseHandler):
    """Handler to create an empty Git repository or reinitialize an existing repository."""

    def post(self):
        """Create an empty Git repository or reinitialize an existing repository.

        Response:
            {
                'code': int,          # command status code
                'message': string     # command results
            }

        """
        res = self.git.init()
        self.finish(res)


class LocalBranches(BaseHandler):
    """Handler for returning a list of local branches."""

    def get(self):
        """Return a list of local branches.

        Response:
            A JSON object having the following format:

            {
                'code': int,             # command status code
                'branches': [...string]  # list of branches
            }

        """
        res = self.git.local_branches()
        self.finish(res)


class Push(BaseHandler):
    """Handler for updating remote refs along with associated objects."""

    def push(self):
        """Update remote refs along with associated objects.

        Fields:
            remote: remote name
            branch: branch name (optional)

        Returns:
            A JSON object having the following format:

            {
                'code': int,          # command status code
                'message': string     # command results
            }

        """
        data = self.get_json_body()
        if 'remote' not in data:
            raise tornado.web.HTTPError(400, 'must provide a remote')

        if 'branch' in data:
            branch = data['branch']
        else:
            branch = None

        res = self.git.push(data['remote'], branch)
        self.finish(res)


def add_handlers(web_app):
    """Add handlers for executing Git commands.

    Args:
        web_app: handle to the Notebook web server instance

    """
    handlers = [
        # Please keep handlers in alphabetical order...
        ('/simple_git/add', AddFiles),
        ('/simple_git/checkout_branch', CheckoutBranch),
        ('/simple_git/commit', Commit),
        ('/simple_git/commit_history', CommitHistory),
        ('/simple_git/current_branch', CurrentBranch),
        ('/simple_git/current_changed_files', CurrentChangedFiles),
        ('/simple_git/delete_branch', DeleteBranch),
        ('/simple_git/delete_untracked_files', DeleteUntrackedFiles),
        ('/simple_git/fetch', Fetch),
        ('/simple_git/init', Init),
        ('/simple_git/local_branches', LocalBranches),
        ('/simple_git/push', Push)
    ]

    # Prefix the base URL to each handler:
    base_url = web_app.settings['base_url']
    handlers = [(url_path_join(base_url, x[0]), x[1]) for x in handlers]

    # Add the handlers to the Notebook server:
    web_app.add_handlers('.*$', handlers)
