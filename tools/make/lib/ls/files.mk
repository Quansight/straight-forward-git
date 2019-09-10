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

# Define the command flags:
FIND_FILES_FLAGS ?= \
	-type f \
	-name "$(FILES_PATTERN)" \
	-regex "$(FILES_FILTER)" \
	$(FIND_EXCLUDE_FLAGS)

ifneq ($(OS), Darwin)
	FIND_FILES_FLAGS := -regextype posix-extended $(FIND_FILES_FLAGS)
endif

# Define a command for finding files:
FIND_FILES_CMD ?= find $(find_kernel_prefix) $(ROOT_DIR) $(FIND_FILES_FLAGS)

# Define the list of files:
FILES ?= $(shell $(FIND_FILES_CMD))


# RULES #

# Lists all files, excluding the `node_modules`, `build`, `reports`, and hidden directories.
#
# @example
# make list-files
#/
list-files:
	$(QUIET) find $(find_kernel_prefix) $(ROOT_DIR) $(FIND_FILES_FLAGS) $(find_print_list)

.PHONY: list-files
