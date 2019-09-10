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

# Define a generic filename pattern:
FILES_PATTERN ?= *

# Define a generic filepath pattern:
FILES_FILTER ?= .*/.*


# Define a filename pattern for source files:
TYPESCRIPT_SOURCES_PATTERN ?= *.$(TYPESCRIPT_FILENAME_EXT)

# Define a filename pattern for Python source files:
PYTHON_SOURCES_PATTERN ?= *.$(PYTHON_FILENAME_EXT)

# Define a filepath pattern for source files:
SOURCES_FILTER ?= .*/.*


# Define a filename pattern for JavaScript files:
JAVASCRIPT_PATTERN ?= *.$(JAVASCRIPT_FILENAME_EXT)

# Define a filepath pattern for JavaScript files:
JAVASCRIPT_FILTER ?= .*/.*


# Define a filename pattern for Markdown files:
MARKDOWN_PATTERN ?= *.$(MARKDOWN_FILENAME_EXT)

# Define a filepath pattern for Markdown files:
MARKDOWN_FILTER ?= .*/.*


# Define a filename pattern for Makefile files:
MAKEFILE_PATTERN ?= *.$(MAKEFILE_FILENAME_EXT)

# Define a file pattern for Makefile files:
MAKEFILE_FILTER ?= .*/.*


# Define a filename pattern for Python files:
PYTHON_PATTERN ?= *.$(PYTHON_FILENAME_EXT)

# Define a filepath pattern for Python files:
PYTHON_FILTER ?= .*/.*


# Define a filename pattern for shell script files:
SHELL_PATTERN ?= *.$(SHELL_FILENAME_EXT)

# Define a filepath pattern for shell script files:
SHELL_FILTER ?= .*/.*


# Define a filename pattern for TypeScript files:
TYPESCRIPT_PATTERN ?= *.$(TYPESCRIPT_FILENAME_EXT)

# Define a filepath pattern for TypeScript files:
TYPESCRIPT_FILTER ?= .*/.*

# Define a filename pattern for TypeScript TSX files:
TYPESCRIPT_TSX_PATTERN ?= *.$(TYPESCRIPT_TSX_FILENAME_EXT)

# Define a filepath pattern for TypeScript TSX files:
TYPESCRIPT_TSX_FILTER ?= .*/.*

# Define a filename pattern for TypeScript declaration files:
TYPESCRIPT_DECLARATIONS_PATTERN ?= *.$(TYPESCRIPT_DECLARATION_FILENAME_EXT)

# Define a filepath pattern for TypeScript declaration files:
TYPESCRIPT_DECLARATIONS_FILTER ?= .*/.*


# Minimum set of exclude flags (Note: order does matter to some degree):
FIND_EXCLUDE_FLAGS ?= \
	-not -path "$(ROOT_DIR)/.git/*" \
	-not -path "$(NODE_MODULES)/*" \
	-not -path "$(BUILD_DIR)/*" \
	-not -path "$(REPORTS_DIR)/*" \
	-not -path "$(TMP_DIR)/*" \
	-not -path "$(ROOT_DIR)/**/$(BUILD_FOLDER)/*" \
	-not -path "$(ROOT_DIR)/**/$(TMP_FOLDER)/*"

# Common exclude flags that most recipes should use (Note: order does matter to some degree):
FIND_COMMON_EXCLUDE_FLAGS ?= \
	-not -path "$(ROOT_DIR)/.*" \
	-not -path "$(NODE_MODULES)/*" \
	-not -path "$(BUILD_DIR)/*" \
	-not -path "$(DEPS_DIR)/*" \
	-not -path "$(REPORTS_DIR)/*" \
	-not -path "$(TMP_DIR)/*" \
	-not -path "$(ROOT_DIR)/**/$(BUILD_FOLDER)/*" \
	-not -path "$(ROOT_DIR)/**/$(TMP_FOLDER)/*"

# Files exclude flags:
FIND_FILES_EXCLUDE_FLAGS ?= $(FIND_COMMON_EXCLUDE_FLAGS)

# Makefile exclude flags:
FIND_MAKEFILES_EXCLUDE_FLAGS ?= $(FIND_EXCLUDE_FLAGS)

# Markdown exclude flags:
FIND_MARKDOWN_EXCLUDE_FLAGS ?= $(FIND_EXCLUDE_FLAGS)

# Sources exclude flags:
FIND_SOURCES_EXCLUDE_FLAGS ?= \
	$(FIND_COMMON_EXCLUDE_FLAGS) \
	-not -path "$(TOOLS_DIR)/*" \
	-not -path "$(ROOT_DIR)/**/$(EXAMPLES_FOLDER)/*" \
	-not -path "$(ROOT_DIR)/**/$(TESTS_FOLDER)/*" \
	-not -path "$(ROOT_DIR)/**/$(DOCUMENTATION_FOLDER)/*" \
	-not -path "$(ROOT_DIR)/**/$(SCRIPTS_FOLDER)/*"

# Tests exclude flags:
FIND_TESTS_EXCLUDE_FLAGS ?= \
	$(FIND_COMMON_EXCLUDE_FLAGS) \
	-not -path "$(TOOLS_DIR)/*" \
	-not -path "$(ROOT_DIR)/**/$(TESTS_FIXTURES_FOLDER)/*"

# Tests directories exclude flags:
FIND_TESTS_DIRS_EXCLUDE_FLAGS ?= \
	$(FIND_COMMON_EXCLUDE_FLAGS) \
	-not -path "$(TOOLS_DIR)/*"

# Text fixtures exclude flags:
FIND_TESTS_FIXTURES_EXCLUDE_FLAGS ?= \
	$(FIND_COMMON_EXCLUDE_FLAGS) \
	-not -path "$(TOOLS_DIR)/*"

# On Mac OSX, in order to use `|` and other regular expression operators, we need to use enhanced regular expression syntax (-E); see https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man7/re_format.7.html#//apple_ref/doc/man/7/re_format.
ifeq ($(OS), Darwin)
	find_kernel_prefix := -E
else
	find_kernel_prefix :=
endif

# Define a suffix for pretty printing results as a list:
find_print_list := -exec printf '%s\n' {} \;


# DEPENDENCIES #

# Note: keep in alphabetical order
include $(TOOLS_MAKE_LIB_DIR)/ls/files.mk
include $(TOOLS_MAKE_LIB_DIR)/ls/make/Makefile
include $(TOOLS_MAKE_LIB_DIR)/ls/python/Makefile
include $(TOOLS_MAKE_LIB_DIR)/ls/typescript/Makefile
