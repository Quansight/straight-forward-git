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

"""Initialize the Jupyter server extension."""

# pylint: disable=W0511

from jupyterlab_simple_git.handlers import add_handlers
from jupyterlab_simple_git.git import Git


def _jupyter_server_extension_paths():
    """Declare the Jupyter server extension paths."""
    return [
        {
            'module': 'jupyterlab_simple_git'
        }
    ]


def _jupyter_nbextension_paths():
    """Declare the Jupyter notebook extension paths."""
    return [
        {
            'section': 'notebook',
            'dest': 'jupyterlab_simple_git'
        }
    ]


def load_jupyter_server_extension(nbapp):
    """Load the Jupyter server extension.

    Args:
        nbapp: handle to the Notebook web server instance

    """
    root = nbapp.web_app.settings.get('server_root_dir')

    # TODO: we assume that the root directory is (or will be) a Git repository. Should we account for it being otherwise?
    nbapp.web_app.settings['simple_git'] = Git(root)
    add_handlers(nbapp.web_app)
