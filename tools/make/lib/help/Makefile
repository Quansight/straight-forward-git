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

# Define the path to the Makefile usage text file for displaying help information:
MAKE_USAGE ?= $(TOOLS_MAKE_DIR)/usage.txt


# RULES #

#/
# Prints a `Makefile` help message which includes a list of common commands.
#
# @example
# make help
#/
help:
	$(QUIET) $(CAT) $(MAKE_USAGE)

.PHONY: help

#/
# Prints a sorted list of `Makefile` rules.
#
# ## Notes
#
# -   The list of rules is **not** exhaustive, as the list does **not** include rules which have not been explicitly declared PHONY targets and does **not** include rules declared via variables. These rules could be included by dumping the Makefile database `make -qp`, but this is not seen as necessary due to predominant use of `.PHONY`.
#
# @example
# make list-rules
#/
list-rules:
	$(QUIET) $(FIND_TOOLS_MAKEFILES_CMD) \
	| xargs grep '^.PHONY: ' \
	| awk '{print $$2}' \
	| sort

.PHONY: list-rules
