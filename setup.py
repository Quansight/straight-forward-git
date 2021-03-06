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

"""jupyter_simple_git setup."""

from setuptools import setup

with open("README.md", "r") as f:
    DESC = f.read()

setup(
    name="jupyterlab_simple_git",
    version="0.0.0",
    description="A Jupyter Notebook server extension that provides a simplified Git interface.",
    long_description=DESC,
    author="Quansight",
    url="https://github.com/Quansight/straight-forward-git",
    license="BSD-3-Clause",
    platforms="Linux, Mac OS X, Windows",
    keywords=[
        "jupyter",
        "jupyterlab",
        "git"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD-3-Clause",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    data_files=[
        # akin to `jupyter serverextension enable --sys-prefix`
        (
            "etc/jupyter/jupyter_server_config.d",
            ["etc/jupyter/jupyter_server_config.d/jupyterlab_simple_git.json"]
        ),
    ],
    install_requires=[]
)
