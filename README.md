# linux-font-installer
install many fonts in one step

### installation
```
git clone https://github.com/mrmoein/linux-font-installer
cd ~
nano .bashrc
```
add this to end of file
```
alias font-installer="python3 /path/to/directory/install-fonts/font-installer.py"
```
**note**: replace `/path/to/directory` with current application path

now you can run `font-installer` commend everywhere