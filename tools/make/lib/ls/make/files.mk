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
FIND_MAKEFILES_FLAGS ?= \
	-type f \
	\( \
		-name 'Makefile' \
		-o \
		-name "$(MAKEFILE_PATTERN)" \
	\) \
	-regex "$(MAKEFILE_FILTER)" \
	$(FIND_MAKEFILES_EXCLUDE_FLAGS)

ifneq ($(OS), Darwin)
	FIND_MAKEFILES_FLAGS := -regextype posix-extended $(FIND_MAKEFILES_FLAGS)
endif

# Define a command for listing Makefile files:
FIND_MAKEFILES_CMD ?= find $(find_kernel_prefix) $(ROOT_DIR) $(FIND_MAKEFILES_FLAGS)

# Define the list of files:
MAKEFILES_FILES ?= $(shell $(FIND_MAKEFILES_CMD))


# RULES #

# Lists all Makefile files.
#
# @example
# make list-makefiles-files
#/
list-makefiles-files:
	$(QUIET) find $(find_kernel_prefix) $(ROOT_DIR) $(FIND_MAKEFILES_FLAGS) $(find_print_list)

.PHONY: list-makefiles-files
