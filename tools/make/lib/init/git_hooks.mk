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

# Define the directory from which to copy Git hooks:
GIT_HOOKS_DIR ?= $(TOOLS_DIR)/git/hooks

# Define a list of hooks:
GIT_HOOKS ?= $(shell find $(GIT_HOOKS_DIR) -type f | xargs -n 1 basename)

# Define the destination directory for Git hooks:
GIT_HOOKS_OUT ?= $(ROOT_DIR)/.git/hooks


# RULES #

#/
# Installs [Git hooks][1].
#
# [1]: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
#
# @example
# make init-git-hooks
#/
init-git-hooks:
	$(QUIET) for file in $(GIT_HOOKS); do \
		$(CP) $(GIT_HOOKS_DIR)/$$file $(GIT_HOOKS_OUT)/$$file; \
		$(MAKE_EXECUTABLE) $(GIT_HOOKS_OUT)/$$file; \
	done

.PHONY: init-git-hooks
