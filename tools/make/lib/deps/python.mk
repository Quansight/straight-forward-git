#/
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
#/

# VARIABLES #

# Define the path to the pip requirements file:
PIP_REQUIREMENTS ?= $(CONFIG_DIR)/python/requirements.txt


# RULES #

#/
# Installs Python dependencies.
#
# @param {string} [PIP_REQUIREMENTS] - path to requirements file (e.g., `/foo/bar/baz/requirements.txt`)
#
# @example
# make install-deps-python
#/
install-deps-python:
	$(QUIET) $(PYTHON) -m pip install --upgrade pip
	$(QUIET) $(PYTHON) -m pip install -r $(PIP_REQUIREMENTS)

.PHONY: install-deps-python

#/
# Updates Python dependencies.
#
# @param {string} [PIP_REQUIREMENTS] - path to requirements file (e.g., `/foo/bar/baz/requirements.txt`)
#
# @example
# make update-deps-python
#/
update-deps-python:
	$(QUIET) $(PYTHON) -m pip install --upgrade pip
	$(QUIET) $(PYTHON) -m pip install --upgrade -r $(PIP_REQUIREMENTS)

.PHONY: update-deps-python

#/
# Uninstalls Python dependencies.
#
# @param {string} [PIP_REQUIREMENTS] - path to requirements file (e.g., `/foo/bar/baz/requirements.txt`)
#
# @example
# make clean-deps-python
#/
clean-deps-python:
	$(QUIET) $(PYTHON) -m pip install --upgrade pip
	$(QUIET) $(PYTHON) -m pip uninstall -r $(PIP_REQUIREMENTS)

.PHONY: clean-deps-python
