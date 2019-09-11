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

"""Script to demonstrate git actions."""

# pylint: disable=C0413

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from jupyterlab_simple_git.git import Git  # noqa


def main():
    """Run the script."""
    cwd = os.getcwd()
    git = Git(cwd)

    # Run a git command:
    res = git.run(args=['help'])
    print(json.dumps(res, indent=4))

    # Attempt to initialize (or reinitialize) a Git repository:
    res = git.init()
    print(json.dumps(res, indent=4))

    # Get the current branch:
    res = git.current_branch()
    print(json.dumps(res, indent=4))

    # Get the current status:
    res = git.status()
    print(json.dumps(res, indent=4))

    # Get the list of current changed files:
    res = git.list_current_changed_files()
    print(json.dumps(res, indent=4))

    # Get the commit history:
    res = git.commit_history(n=2)  # last two commits
    print(json.dumps(res, indent=4))

    # Add this file to the working tree:
    res = git.add(__file__)
    print(json.dumps(res, indent=4))

    # Remove this file from the working tree:
    res = git.reset(__file__)
    print(json.dumps(res, indent=4))

    # Checkout the current branch (no-op):
    res = git.checkout_branch(git.current_branch()['branch'])
    print(json.dumps(res, indent=4))

    # Attempt to delete a non-existent branch:
    res = git.delete_branch('foo_bar_biz_bap')
    print(json.dumps(res, indent=4))

    # Checkout a new branch:
    branch = git.current_branch()['branch']
    res = git.checkout_branch('foo_bar_biz_bap')
    print(json.dumps(res, indent=4))

    # Switch back to the previous branch:
    res = git.checkout_branch(branch)
    print(json.dumps(res, indent=4))

    # Delete the new branch:
    res = git.delete_branch('foo_bar_biz_bap')
    print(json.dumps(res, indent=4))


if __name__ == "__main__":
    main()
