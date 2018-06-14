## Update trellis

Clone Fatsoma fork of trellis to your preferred location or pull the latest changes if you already have a clone.

```sh
git clone git@github.com:Fatsoma/trellis.git $TRELLIS_DIR
```

Copy files from trellis into your project trellis directory (run from your clone of trellis):

```sh
PROJECT_DIR=~/code/wp    # set to your project directory

rsync -av --exclude-from .rsync-exclude ./ "${PROJECT_DIR}/trellis"
```

Check the changes made to files in `group_vars` - particularly for deletions as
these are likely things that were added in the project:

```sh
git diff group_vars
```

Manually check for differences in:

```
group_vars/all/main.yml
group_vars/all/users.yml
vagrant.default.yml
```
