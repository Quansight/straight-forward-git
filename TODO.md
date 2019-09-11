# TODO

1.  Add `development.md` guide in `/docs` (e.g., `make init`, etc)
2.  Setup tsdoc generation
3.  Add support for bash linting via shellcheck
4.  Determine the correct value for `install_requires` in `setup.py` (e.g., why `notebook` and not `jupyterlab`?)
5.  Setup TypeScript linting on pre-commit
6.  git commands
    -   config (get/set)
        -   why? to allow for admins to set the remote, etc
        -   hmm...I think this may be too complex/unneeded
    -   commit
    -   pull (how to deal with merge conflicts? see https://www.gitkraken.com/git-client for possible inspiration)
    -   fetch (in order to have access to branches created and pushed by collaborators)
    -   push
    -   list number of changes (additions, deletions, etc)
    -   new branch
    -   switch branch
    -   diff
    -   add
        -   file
        -   all
    -   reset
        -   file
        -   all
    -   init
