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
# @param {string} [PYTHON_PACKAGE_INSTALLER] - name of Python package installer (e.g., `pip`)
# @param {string} [PIP_REQUIREMENTS] - path to requirements file (e.g., `/foo/bar/baz/requirements.txt`)
#
# @example
# make install-python-packages
#/
install-python-packages:
ifeq ($(PYTHON_PACKAGE_INSTALLER), pip)
	$(QUIET) $(PYTHON) -m pip install --upgrade pip
	$(QUIET) $(PYTHON) -m pip install -r $(PIP_REQUIREMENTS)
else
ifeq ($(PYTHON_PACKAGE_INSTALLER), conda)
	$(QUIET) $(CONDA) install -y --file $(PIP_REQUIREMENTS)
endif
endif

.PHONY: install-python-packages

#/
# Updates Python dependencies.
#
# @param {string} [PYTHON_PACKAGE_INSTALLER] - name of Python package installer (e.g., `pip`)
# @param {string} [PIP_REQUIREMENTS] - path to requirements file (e.g., `/foo/bar/baz/requirements.txt`)
#
# @example
# make update-python-packages
#/
update-python-packages:
ifeq ($(PYTHON_PACKAGE_INSTALLER), pip)
	$(QUIET) $(PYTHON) -m pip install --upgrade pip
	$(QUIET) $(PYTHON) -m pip install --upgrade -r $(PIP_REQUIREMENTS)
else
ifeq ($(PYTHON_PACKAGE_INSTALLER), conda)
	$(QUIET) $(CONDA) install -y --file $(PIP_REQUIREMENTS)
endif
endif

.PHONY: update-python-packages

#/
# Uninstalls Python dependencies.
#
# @param {string} [PYTHON_PACKAGE_INSTALLER] - name of Python package installer (e.g., `pip`)
# @param {string} [PIP_REQUIREMENTS] - path to requirements file (e.g., `/foo/bar/baz/requirements.txt`)
#
# @example
# make clean-python-packages
#/
clean-python-packages:
ifeq ($(PYTHON_PACKAGE_INSTALLER), pip)
	$(QUIET) $(PYTHON) -m pip install --upgrade pip
	$(QUIET) $(PYTHON) -m pip uninstall -r $(PIP_REQUIREMENTS)
else
ifeq ($(PYTHON_PACKAGE_INSTALLER), conda)
	$(QUIET) $(CAT) $(PIP_REQUIREMENTS) | while read -r package; do \
		$(CONDA) remove -y $$package || exit 1; \
	done
endif
endif

.PHONY: clean-python-packages
