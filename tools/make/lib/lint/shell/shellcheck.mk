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

# Define the command-line options to use when invoking the shellcheck executable:
SHELLCHECK_FLAGS ?=


# RULES #

#/
# Checks whether [shellcheck][1] is installed.
#
# [1]: https://github.com/koalaman/shellcheck
#
# @private
#
# @example
# make check-shellcheck
#/
check-shellcheck:
ifeq (, $(shell command -v $(SHELLCHECK) 2>/dev/null))
	$(QUIET) echo ''
	$(QUIET) echo 'shellcheck is not installed. Please install shellcheck and try again.'
	$(QUIET) echo 'For install instructions, see https://github.com/koalaman/shellcheck'
	$(QUIET) echo 'and the project development guide.'
	$(QUIET) echo ''
	$(QUIET) exit 1
else
	$(QUIET) echo 'shellcheck is installed.'
	$(QUIET) exit 0
endif

.PHONY: check-shellcheck

#/
# Lints shell script files using [shellcheck][1].
#
# ## Notes
#
# -   This rule is useful when wanting to glob for files, irrespective of context, for a particular directory in order to lint all contained shell script files.
#
# [1]: https://github.com/koalaman/shellcheck
#
# @private
# @param {string} [SHELL_FILTER] - file path pattern (e.g., `.*/_tools/.*`)
# @param {*} [FAST_FAIL] - flag indicating whether to stop linting upon encountering a lint error
#
# @example
# make shellcheck
#
# @example
# make shellcheck SHELL_FILTER=.*/_tools/.*
#/
shellcheck:
ifeq ($(FAIL_FAST), true)
	$(QUIET) $(FIND_SHELL_CMD) | grep '^[\/]\|^[a-zA-Z]:[/\]' | while read -r file; do \
		echo ''; \
		echo "Linting file: $$file"; \
		$(SHELLCHECK) $(SHELLCHECK_FLAGS) $$file || exit 1; \
	done
else
	$(QUIET) $(FIND_SHELL_CMD) | grep '^[\/]\|^[a-zA-Z]:[/\]' | while read -r file; do \
		echo ''; \
		echo "Linting file: $$file"; \
		$(SHELLCHECK) $(SHELLCHECK_FLAGS) $$file || echo 'Linting failed.'; \
	done
endif

.PHONY: shellcheck

#/
# Lints a specified list of shell script files using [shellcheck][1].
#
# ## Notes
#
# -   This rule is useful when wanting to lint a list of shell script files generated by some other command (e.g., a list of changed shell script files obtained via `git diff`).
#
# [1]: https://github.com/koalaman/shellcheck
#
# @private
# @param {string} FILES - list of shell script file paths
# @param {*} [FAST_FAIL] - flag indicating whether to stop linting upon encountering a lint error
#
# @example
# make shellcheck-files FILES='/foo/file.sh /bar/file.sh'
#/
shellcheck-files:
ifeq ($(FAIL_FAST), true)
	$(QUIET) for file in $(FILES); do \
		echo ''; \
		echo "Linting file: $$file"; \
		$(SHELLCHECK) $(SHELLCHECK_FLAGS) $$file || exit 1; \
	done
else
	$(QUIET) for file in $(FILES); do \
		echo ''; \
		echo "Linting file: $$file"; \
		$(SHELLCHECK) $(SHELLCHECK_FLAGS) $$file || echo 'Linting failed.'; \
	done
endif

.PHONY: shellcheck-files