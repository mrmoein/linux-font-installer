import os

if os.geteuid() != 0:
    print('you must be root!')

else:
    # create shell file for accessing program from terminal
    font_installer_path = os.path.dirname(os.path.realpath(__file__)) + '/font-installer.py'

    bash_file = "#i/bin/sh\n" \
                f"python3 {font_installer_path} $@"

    f = open('/bin/font-installer', 'w')
    f.write(bash_file)
    f.close()

    # make file executable
    os.system('sudo chmod +x /bin/font-installer')

    print('done')
