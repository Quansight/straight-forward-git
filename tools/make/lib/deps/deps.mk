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

# Define the path for saving dependency downloads:
DEPS_TMP_DIR ?= $(DEPS_DIR)/tmp

# Define the path for dependency checksums:
DEPS_CHECKSUMS_DIR ?= $(DEPS_DIR)/checksums

# Define the path to an executable for downloading a remote resource:
DEPS_DOWNLOAD_BIN ?= $(TOOLS_DIR)/scripts/download

# Define the path to an executable for verifying a download:
DEPS_CHECKSUM_BIN ?= $(TOOLS_DIR)/scripts/checksum


# DEPENDENCIES #

include $(TOOLS_MAKE_LIB_DIR)/deps/shellcheck.mk


# RULES #

#/
# Creates directory for storing external library downloads.
#
# @private
#/
$(DEPS_TMP_DIR):
	$(QUIET) $(MKDIR_RECURSIVE) $(DEPS_TMP_DIR)

#/
# Creates directory for storing external libraries.
#
# @private
#/
$(DEPS_BUILD_DIR):
	$(QUIET) $(MKDIR_RECURSIVE) $(DEPS_BUILD_DIR)

#/
# Installs external library dependencies.
#
# @example
# make install-deps
#/
install-deps: install-deps-shellcheck

.PHONY: install-deps

#/
# Removes external libraries.
#
# @example
# make clean-deps
#/
clean-deps: clean-deps-downloads clean-deps-build clean-deps-tests

.PHONY: clean-deps

#/
# Removes external library builds.
#
# @example
# make clean-deps-build
#/
clean-deps-build:
	$(QUIET) $(DELETE) $(DELETE_FLAGS) $(DEPS_BUILD_DIR)

.PHONY: clean-deps-build

#/
# Removes external library installation tests.
#
# @example
# make clean-deps-tests
#/
clean-deps-tests:

.PHONY: clean-deps-tests

#/
# Removes external library downloads.
#
# @example
# make clean-deps-downloads
#/
clean-deps-downloads:
	$(QUIET) $(DELETE) $(DELETE_FLAGS) $(DEPS_TMP_DIR)

.PHONY: clean-deps-downloads
