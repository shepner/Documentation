#!/bin/sh

git pull origin master

# git init
git add .

# this is needed only if there was a .git dir someplace it shouldnt have been:
# `git rm --cached path_to_submodule`

git status

git commit -m 'automatic update'
#git remote add origin https://github.com/shepner/Documentation
#git push --force -u origin master
git push -u origin master

