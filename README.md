# linux-font-installer
Install all fonts in a directory with one command

for subtitle fonts and other usege

### installation
```
git clone https://github.com/mrmoein/linux-font-installer
cd ~
nano .bashrc
```
add this to end of file
```
alias font-installer="python3 /path/to/directory/linux-font-installer/font-installer.py"
```
>**note**: replace `/path/to/directory` with current application path

now you can run `font-installer` commend everywhere

go to directory that contain fonts and run `font-installer`

### right click install for linux mint
if you use nemo file manger, you can add the `font-installer.nemo_action` to `~/.local/share/nemo/actions` directory

> **note**: replace `Exec=python3 /path/to/directory/font-installer.py %F` with the `font-installer.py` path (do not remove %F)

now close and open nemo(file manger)

![nemo action screenshot](nemo_action_screenshot.png)