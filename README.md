# jupyterlab-simple-git

Simplified git extension for Jupyterlab.

## Prerequisites

-   JupyterLab

## Installation

```bash
$ pip install jupyterlab_simple_git
$ jupyter labextension install jupyterlab-simple-git
```

## Development

For a development install, do the following in the repository directory:

```bash
$ make init
$ make install
$ npm run build
$ jupyter labextension link .
```

To rebuild the package and the JupyterLab app:

```bash
$ npm run build
$ jupyter lab build
```

## Editors

-   This repository uses [EditorConfig][editorconfig] to maintain consistent coding styles between different editors and IDEs, including [browsers][editorconfig-chrome].

<section class="links">

[editorconfig]: http://editorconfig.org/

[editorconfig-chrome]: https://chrome.google.com/webstore/detail/github-editorconfig/bppnolhdpdfmmpeefopdbpmabdpoefjh?hl=en-US

</section>

<!-- ./links -->

