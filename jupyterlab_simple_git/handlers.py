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
            path: a subdirectory path, file path, glob, or a list of paths and/or globs
            update_all: boolean indicating whether to update all entries in the index to match the working tree

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

        res = self.git.add(path=path, update_all=update_all)
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
        res = self.git.checkout_branch(data['branch'])
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


def add_handlers(web_app):
    """Add handlers for executing Git commands.

    Args:
        web_app: handle to the Notebook web server instance

    """
    handlers = [
        # Please keep handlers in alphabetical order...
        ('/simple_git/add', AddFiles),
        ('/simple_git/checkout_branch', CheckoutBranch),
        ('/simple_git/current_changed_files', CurrentChangedFiles)
    ]

    # Prefix the base URL to each handler:
    base_url = web_app.settings['base_url']
    handlers = [(url_path_join(base_url, x[0]), x[1]) for x in handlers]

    # Add the handlers to the Notebook server:
    web_app.add_handlers('.*$', handlers)
