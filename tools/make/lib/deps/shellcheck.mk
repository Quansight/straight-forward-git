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

# Define the download URL...
ifeq ($(OS), WINNT)
	DEPS_SHELLCHECK_URL ?= https://shellcheck.storage.googleapis.com/shellcheck-v$(DEPS_SHELLCHECK_VERSION).zip
else
	DEPS_SHELLCHECK_URL ?= https://shellcheck.storage.googleapis.com/shellcheck-v$(DEPS_SHELLCHECK_VERSION).linux.x86_64.tar.xz
endif

# Determine the basename for the download:
deps_shellcheck_basename := $(notdir $(DEPS_SHELLCHECK_URL))

# Define the path to the file containing a checksum verify a download:
DEPS_SHELLCHECK_CHECKSUM ?= $(shell cat $(DEPS_CHECKSUMS_DIR)/$(subst .,_,$(subst -,_,$(deps_shellcheck_basename)))/sha256)

# Define the output path when downloading:
DEPS_SHELLCHECK_DOWNLOAD_OUT ?= $(DEPS_TMP_DIR)/$(deps_shellcheck_basename)

# Define the output path after extracting:
deps_shellcheck_extract_out := $(DEPS_BUILD_DIR)/shellcheck-v$(DEPS_SHELLCHECK_VERSION)

# Define the path to the `shellcheck` executable...
ifeq ($(DEPS_SHELLCHECK_PLATFORM), darwin)
	# We assume that `shellcheck` is installed globally:
	SHELLCHECK ?= shellcheck
else
	SHELLCHECK ?= $(DEPS_SHELLCHECK_BUILD_OUT)/shellcheck
endif

# Define rule prerequisites based on the host platform...
ifeq ($(DEPS_SHELLCHECK_PLATFORM), darwin)
	deps_shellcheck_test_prereqs :=
	deps_shellcheck_install_prereqs := deps-install-shellcheck-darwin deps-test-shellcheck
else
	deps_shellcheck_test_prereqs := $(DEPS_SHELLCHECK_BUILD_OUT)
	deps_shellcheck_install_prereqs := deps-download-shellcheck deps-verify-shellcheck deps-extract-shellcheck deps-test-shellcheck
endif


# RULES #

#/
# Downloads a shellcheck distribution.
#
# @private
#/
$(DEPS_SHELLCHECK_DOWNLOAD_OUT): | $(DEPS_TMP_DIR)
	$(QUIET) echo 'Downloading shellcheck...' >&2
	$(QUIET) $(DEPS_DOWNLOAD_BIN) $(DEPS_SHELLCHECK_URL) $(DEPS_SHELLCHECK_DOWNLOAD_OUT)

#/
# Extracts a shellcheck archive.
#
# @private
#/
$(DEPS_SHELLCHECK_BUILD_OUT): $(DEPS_SHELLCHECK_DOWNLOAD_OUT) | $(DEPS_BUILD_DIR)
ifeq ($(OS), WINNT)
	$(QUIET) echo 'Extracting shellcheck...' >&2
	$(QUIET) $(UNZIP) -q $(DEPS_SHELLCHECK_DOWNLOAD_OUT) -d $@
else
	$(QUIET) echo 'Extracting shellcheck...' >&2
	$(QUIET) $(TAR) --xz -xvf $(DEPS_SHELLCHECK_DOWNLOAD_OUT) -C $(DEPS_BUILD_DIR)
	$(QUIET) mv $(deps_shellcheck_extract_out) $(DEPS_SHELLCHECK_BUILD_OUT)
endif

#/
# Downloads shellcheck.
#
# @example
# make deps-download-shellcheck
#/
deps-download-shellcheck: $(DEPS_SHELLCHECK_DOWNLOAD_OUT)

.PHONY: deps-download-shellcheck

#/
# Verifies a shellcheck download.
#
# @example
# make deps-verify-shellcheck
#/
deps-verify-shellcheck: deps-download-shellcheck
	$(QUIET) echo 'Verifying download...' >&2
	$(QUIET) $(DEPS_CHECKSUM_BIN) $(DEPS_SHELLCHECK_DOWNLOAD_OUT) $(DEPS_SHELLCHECK_CHECKSUM) >&2

.PHONY: deps-verify-shellcheck

#/
# Extracts a shellcheck download.
#
# @example
# make deps-extract-shellcheck
#/
deps-extract-shellcheck: $(DEPS_SHELLCHECK_BUILD_OUT)

.PHONY: deps-extract-shellcheck

#/
# Tests a shellcheck installation.
#
# @example
# make deps-test-shellcheck
#/
deps-test-shellcheck: $(deps_shellcheck_test_prereqs)
	$(QUIET) echo 'Running tests...' >&2
	$(QUIET) $(SHELLCHECK) --version >&2
	$(QUIET) echo '' >&2
	$(QUIET) echo 'Success.' >&2

.PHONY: deps-test-shellcheck

#/
# Installs shellcheck on MacOS.
#
# ## Notes
#
# -   We **assume** that [Homebrew][1] is installed.
#
# [1]: https://brew.sh/
#
# @private
# @example
# make deps-install-shellcheck-darwin
#/
deps-install-shellcheck-darwin:
	$(QUIET) echo 'Installing shellcheck...' >&2
	$(QUIET) brew update
	$(QUIET) brew install shellcheck

.PHONY: deps-install-shellcheck-darwin

#/
# Installs shellcheck.
#
# @example
# make install-deps-shellcheck
#/
install-deps-shellcheck: $(deps_shellcheck_install_prereqs)

.PHONY: install-deps-shellcheck

#/
# Removes a shellcheck distribution (but does not remove a shellcheck download if one exists).
#
# @example
# make clean-deps-shellcheck
#/
clean-deps-shellcheck:
	$(QUIET) $(DELETE) $(DELETE_FLAGS) $(DEPS_SHELLCHECK_BUILD_OUT)

.PHONY: clean-deps-shellcheck
