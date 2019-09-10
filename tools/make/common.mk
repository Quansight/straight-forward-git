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

# VERBOSITY #

ifndef VERBOSE
	QUIET := @
else
	QUIET :=
endif


# GENERAL VARIABLES #

# Define a license SPDX identifier whitelist:
LICENSES_WHITELIST ?= 'Apache-2.0,Artistic-2.0,BSD-2-Clause,BSD-3-Clause,BSL-1.0,CC0-1.0,ISC,MIT,MPL-2.0,Unlicense,WTFPL'

# Define keywords identifying source annotations:
KEYWORDS ?= 'TODO|FIXME|WARNING|HACK|NOTE|OPTIMIZE'

# Indicate whether to "fast" fail when linting, running tests, etc:
ifndef FAST_FAIL
	FAIL_FAST := true
else
ifeq ($(FAST_FAIL), 0)
	FAIL_FAST := false
else
	FAIL_FAST := true
endif
endif


# ENVIRONMENTS #

# Determine the OS:
#
# [1]: https://en.wikipedia.org/wiki/Uname#Examples
# [2]: http://stackoverflow.com/a/27776822/2225624
OS ?= $(shell uname)
ifneq (, $(findstring MINGW,$(OS)))
	OS := WINNT
else
ifneq (, $(findstring MSYS,$(OS)))
	OS := WINNT
else
ifneq (, $(findstring CYGWIN,$(OS)))
	OS := WINNT
else
ifneq (, $(findstring Windows_NT,$(OS)))
	OS := WINNT
endif
endif
endif
endif


# OPTIONS #

# Define the linter to use when linting shell script files:
SHELL_LINTER ?= shellcheck

# Define the installer to use when installing Python packages:
PYTHON_PACKAGE_INSTALLER ?= conda


# COMMANDS #

# Define whether delete operations should be safe (i.e., deleted items are sent to trash, rather than permanently deleted):
SAFE_DELETE ?= false

# Define the delete command:
ifeq ($(SAFE_DELETE), true)
	# FIXME: -rm -rf
	DELETE := -rm
	DELETE_FLAGS := -rf
else
	DELETE ?= -rm
	DELETE_FLAGS ?= -rf
endif

# Define the command for setting executable permissions:
MAKE_EXECUTABLE ?= chmod +x

# Define the command for recursively creating directories (WARNING: portability issues on some systems!):
MKDIR_RECURSIVE ?= mkdir -p

# Define the command for extracting tarfiles:
TAR ?= tar

# Define the command for extracting files compressed in a ZIP archive:
UNZIP ?= unzip

# Define the command to `cat` a file:
CAT ?= cat

# Define the command to copy files:
CP ?= cp

# Define the `git` command:
GIT ?= git

# Define the command for staging files:
GIT_ADD ?= $(GIT) add

# Define the command for committing files:
GIT_COMMIT ?= $(GIT) commit

# Define the command for determining the current commit hash:
GIT_COMMIT_HASH ?= $(GIT) rev-parse HEAD

# Define the command for determining the current branch:
GIT_BRANCH ?= $(GIT) rev-parse --abbrev-ref HEAD

# Determine the `open` command:
ifeq ($(OS), Darwin)
	OPEN ?= open
else
	OPEN ?= xdg-open
endif
# TODO: add Windows command

# Define the command for `node`:
NODE ?= node

# Define the command for `npm`:
NPM ?= npm

# Define the command for `python`:
PYTHON ?= python

# Define the command for `pip`:
PIP ?= pip

# Define the command for `conda`:
CONDA ?= conda

# Define the command for determining the host platform:
NODE_HOST_PLATFORM ?= $(NODE) -e 'console.log( process.platform )'


# EXTERNAL DEPENDENCIES #

# Define the shellcheck version:
DEPS_SHELLCHECK_VERSION ?= 0.5.0

# Generate a version slug:
deps_shellcheck_version_slug := $(subst .,_,$(DEPS_SHELLCHECK_VERSION))

# Define the output path when building shellcheck:
DEPS_SHELLCHECK_BUILD_OUT ?= $(DEPS_BUILD_DIR)/shellcheck_$(deps_shellcheck_version_slug)

# Host platform:
DEPS_SHELLCHECK_PLATFORM := $(shell command -v $(NODE) >/dev/null 2>&1 && $(NODE_HOST_PLATFORM))
