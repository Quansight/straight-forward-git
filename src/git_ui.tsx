/**
* @license BSD-3-Clause
*
* Copyright (c) 2019 Quansight. All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*
* 1. Redistributions of source code must retain the above copyright notice, this
*    list of conditions and the following disclaimer.
*
* 2. Redistributions in binary form must reproduce the above copyright notice,
*    this list of conditions and the following disclaimer in the documentation
*    and/or other materials provided with the distribution.
*
* 3. Neither the name of the copyright holder nor the names of its
*    contributors may be used to endorse or promote products derived from
*    this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
* FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
* DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
* SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
* CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
* OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
* OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

// MODULES //

import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';


// MAIN //

/**
* Widget class which adds a Git tab to the left panel.
*
* @private
*/
class GitTabWidget extends ReactWidget {
	/**
	* Constructor.
	*
	* @returns widget instance
	*/
	constructor() {
		super();
	}

	/**
	* Renders the React component.
	*
	* @returns React element(s)
	*/
	protected render(): React.ReactElement<any> | React.ReactElement<any>[] {
		return (
			<div style={this.styles['jp-git-window']}>
				<h1>Simple Git</h1>
			</div>
		);
	}

	/**
	* CSS styles.
	*/
	styles = {
		'jp-git-window': {
			'background': 'var(--jp-layout-color1)',
			'fontFamily': 'var(--jp-content-font-family)',
			'height': '100%'
		}
	};
}


// EXPORTS //

export default GitTabWidget;
