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

# Determine the filename:
this_file := $(lastword $(MAKEFILE_LIST))

# Determine the absolute path of the Makefile (see http://blog.jgc.org/2007/01/what-makefile-am-i-in.html):
this_dir := $(dir $(CURDIR)/$(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST)))

# Remove the trailing slash:
this_dir := $(patsubst %/,%,$(this_dir))

# Define the root project directory:
ROOT_DIR ?= $(this_dir)

# Define the root tools directory:
TOOLS_DIR ?= $(ROOT_DIR)/tools

# Define the directory containing the entry point for Makefile dependencies:
TOOLS_MAKE_DIR ?= $(TOOLS_DIR)/make

# Define the subdirectory containing Makefile dependencies:
TOOLS_MAKE_LIB_DIR ?= $(TOOLS_MAKE_DIR)/lib

# Define the root build directory:
BUILD_DIR ?= $(ROOT_DIR)/build

# Define the root directory for storing temporary files:
TMP_DIR ?= $(ROOT_DIR)/tmp

# Define the root configuration directory:
CONFIG_DIR ?= $(ROOT_DIR)/etc

# Define the directory for writing reports, including code coverage:
REPORTS_DIR ?= $(ROOT_DIR)/reports
COVERAGE_DIR ?= $(REPORTS_DIR)/coverage

# Define the directory for documentation:
DOCS_DIR ?= $(ROOT_DIR)/docs

# Define the directory for generated source code documentation:
SRC_DOCS_DIR ?= $(BUILD_DIR)/docs

# Define the directory for instrumented source code:
COVERAGE_INSTRUMENTATION_DIR ?= $(BUILD_DIR)/coverage

# Define the top-level directory containing executables:
LOCAL_BIN_DIR ?= $(ROOT_DIR)/bin

# Define the top-level directory containing vendor dependencies:
DEPS_DIR ?= $(ROOT_DIR)/deps

# Define the path to the root `package.json`:
ROOT_PACKAGE_JSON ?= $(ROOT_DIR)/package.json

# Define the top-level directory containing node module dependencies:
NODE_MODULES ?= $(ROOT_DIR)/node_modules

# Define the folder name convention for node module dependencies:
NODE_MODULES_FOLDER ?= node_modules

# Define the top-level directory containing node module executables:
BIN_DIR ?= $(NODE_MODULES)/.bin

# Define the folder name convention for source files:
SOURCE_FOLDER ?= lib

# Define the folder name convention for source files requiring compilation:
SRC_FOLDER ?= src

# Define the folder name convention for test files:
TESTS_FOLDER ?= test

# Define the folder name convention for test fixtures:
TESTS_FIXTURES_FOLDER ?= $(TESTS_FOLDER)/fixtures

# Define the folder name convention for examples files:
EXAMPLES_FOLDER ?= examples

# Define the folder name convention for examples fixtures:
EXAMPLES_FIXTURES_FOLDER ?= $(EXAMPLES_FOLDER)/fixtures

# Define the folder name convention for executables:
BIN_FOLDER ?= bin

# Define the folder name convention for documentation files:
DOCUMENTATION_FOLDER ?= docs

# Define the folder name convention for configuration files:
CONFIG_FOLDER ?= etc

# Define the folder name convention for build artifacts:
BUILD_FOLDER ?= build

# Define the folder name convention for data files:
DATA_FOLDER ?= data

# Define the folder name convention for scripts:
SCRIPTS_FOLDER ?= scripts

# Define the folder name convention for temporary files:
TMP_FOLDER ?= tmp

# Define filename extension conventions (keep in alphabetical order):
BASH_FILENAME_EXT ?= sh
CSS_FILENAME_EXT ?= css
CSV_FILENAME_EXT ?= csv
HTML_FILENAME_EXT ?= html
JAVASCRIPT_FILENAME_EXT ?= js
JPEG_FILENAME_EXT ?= jpg
JSON_FILENAME_EXT ?= json
MAKEFILE_FILENAME_EXT ?= mk
MARKDOWN_FILENAME_EXT ?= md
PNG_FILENAME_EXT ?= png
PYTHON_FILENAME_EXT ?= py
SHELL_FILENAME_EXT ?= sh
SVG_FILENAME_EXT ?= svg
TEXT_FILENAME_EXT ?= txt
TYPESCRIPT_FILENAME_EXT ?= ts
TYPESCRIPT_TSX_FILENAME_EXT ?= tsx
TYPESCRIPT_DECLARATION_FILENAME_EXT ?= d.$(TYPESCRIPT_FILENAME_EXT)
YAML_FILENAME_EXT ?= yml


# DEPENDENCIES #

include $(TOOLS_MAKE_DIR)/Makefile
