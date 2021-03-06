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

# Define the path to the [pycodestyle][1] executable.
#
# To install pycodestyle:
#
# ```bash
# $ pip install pycodestyle
# ```
#
# [1]: https://github.com/PyCQA/pycodestyle
PYCODESTYLE ?= pycodestyle

# Define the path to the pycodestyle configuration file:
PYCODESTYLE_CONF ?= $(CONFIG_DIR)/pycodestyle/.pycodestyle

# Define the command-line options to use when invoking the pycodestyle executable:
PYCODESTYLE_FLAGS ?= \
	--config $(PYCODESTYLE_CONF)


# RULES #

#/
# Checks whether [pycodestyle][1] is installed.
#
# [1]: https://github.com/PyCQA/pycodestyle
#
# @private
#
# @example
# make check-pycodestyle
#/
check-pycodestyle:
ifeq (, $(shell command -v $(PYCODESTYLE) 2>/dev/null))
	$(QUIET) echo ''
	$(QUIET) echo 'pycodestyle is not installed. Please install pycodestyle and try again.'
	$(QUIET) echo 'For install instructions, see https://github.com/PyCQA/pycodestyle.'
	$(QUIET) echo ''
	$(QUIET) exit 1
else
	$(QUIET) echo 'pycodestyle is installed.'
	$(QUIET) exit 0
endif

.PHONY: check-pycodestyle

#/
# Lints Python source code style.
#
# ## Notes
#
# -   This rule is useful when wanting to glob for Python source files (e.g., lint all Python source files in a particular directory).
#
# @private
# @param {string} [PYTHON_SOURCES_FILTER] - file path pattern (e.g., `.*/foo/bar/.*`)
# @param {*} [FAST_FAIL] - flag indicating whether to stop linting upon encountering a lint error
#
# @example
# make pycodestyle-src
#
# @example
# make pycodestyle-src PYTHON_SOURCES_FILTER=.*/foo/bar/.*
#/
pycodestyle-src:
ifeq ($(FAIL_FAST), true)
	$(QUIET) $(FIND_PYTHON_SOURCES_CMD) | grep '^[\/]\|^[a-zA-Z]:[/\]' | while read -r file; do \
		echo ''; \
		echo "Linting code style: $$file"; \
		$(PYCODESTYLE) $(PYCODESTYLE_FLAGS) $$file || exit 1; \
	done
else
	$(QUIET) $(FIND_PYTHON_SOURCES_CMD) | grep '^[\/]\|^[a-zA-Z]:[/\]' | while read -r file; do \
		echo ''; \
		echo "Linting code style: $$file"; \
		$(PYCODESTYLE) $(PYCODESTYLE_FLAGS) $$file || echo 'Linting failed.'; \
	done
endif

.PHONY: pycodestyle-src

#/
# Lints code style for a specified list of Python files.
#
# ## Notes
#
# -   This rule is useful when wanting to lint a list of Python files generated by some other command (e.g., a list of changed Python files obtained via `git diff`).
#
# @private
# @param {string} FILES - list of Python file paths
# @param {*} [FAST_FAIL] - flag indicating whether to stop linting upon encountering a lint error
#
# @example
# make pycodestyle-files FILES='/foo/file.py /bar/file.py'
#/
pycodestyle-files:
ifeq ($(FAIL_FAST), true)
	$(QUIET) for file in $(FILES); do \
		echo ''; \
		echo "Linting code style: $$file"; \
		$(PYCODESTYLE) $(PYCODESTYLE_FLAGS) $$file || exit 1; \
	done
else
	$(QUIET) for file in $(FILES); do \
		echo ''; \
		echo "Linting code style: $$file"; \
		$(PYCODESTYLE) $(PYCODESTYLE_FLAGS) $$file || echo 'Linting failed.'; \
	done
endif

.PHONY: pycodestyle-files
