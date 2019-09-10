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

# RULES #

#/
# Installs node module dependencies.
#
# ## Notes
#
# -   Packages will be [installed][1] in a local `node_modules` directory relative to the project's `package.json` file.
#
# [1]: https://docs.npmjs.com/cli/install
#
# @param {string} [NODE_MODULE_INSTALLER] - name of Node.js node module installer (e.g., `npm`)
#
# @example
# make install-node-modules
#/
install-node-modules: $(ROOT_PACKAGE_JSON)
ifeq ($(NODE_MODULE_INSTALLER), npm)
	$(QUIET) $(NPM) install
else
ifeq ($(NODE_MODULE_INSTALLER), yarn)
	$(QUIET) $(YARN) install
endif
endif

.PHONY: install-node-modules

#/
# De-duplicates node module dependencies.
#
# ## Notes
#
# -   This rule searches the local package tree and attempts to simplify the overall structure by moving dependencies further up the tree, where they can be more effectively shared by multiple dependent packages.
#
# @param {string} [NODE_MODULE_INSTALLER] - name of Node.js node module installer (e.g., `npm`)
#
# @example
# make dedupe-node-modules
#/
dedupe-node-modules: $(NODE_MODULES)
ifeq ($(NODE_MODULE_INSTALLER), npm)
	$(QUIET) $(NPM) dedupe
else
ifeq ($(NODE_MODULE_INSTALLER), yarn)
	$(QUIET) $(YARN) install
endif
endif

.PHONY: dedupe-node-modules

#/
# Removes node module dependencies.
#
# @example
# make clean-node-modules
#/
clean-node-modules:
	$(QUIET) $(DELETE) $(DELETE_FLAGS) $(NODE_MODULES)

.PHONY: clean-node-modules
