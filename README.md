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

For a development install (requires npm version 4 or later), do the following in the repository directory:

```bash
$ npm install
$ npm run build
$ jupyter labextension link .
```

To rebuild the package and the JupyterLab app:

```bash
$ npm run build
$ jupyter lab build
```

