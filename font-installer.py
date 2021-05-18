import os
import sys
import pathlib
import shutil
import subprocess
from fontTools import ttLib
from termcolor import colored


class FontInstaller:
    def __init__(self):
        self.FONT_SPECIFIER_NAME_ID = 4
        self.FONT_SPECIFIER_FAMILY_ID = 1
        self.fonts_post_fix = [".ttf", '.TTF', ".otf", ".OTF"]
        self.DESTINATION_FONTS_PATH = '{home_path}/.local/share/fonts/font-installer-by-moein'.format(
            home_path=os.path.expanduser("~"))
        # create destination fonts directory if not exist
        if not os.path.exists(self.DESTINATION_FONTS_PATH):
            pathlib.Path(self.DESTINATION_FONTS_PATH).mkdir(parents=True, exist_ok=True)
        self.CURRENT_PATH = os.getcwd()

    def ttf_obj_to_name(self, font_obj):
        """
        Description: convert font ttf obj from fontTool lib to 'name' and 'family'
        From: https://gist.github.com/pklaus/dce37521579513c574d0
        Input: fontTools.ttLib.ttFont.TTFont => class
        Return: name => str, family => str
        """
        name = ""
        family = ""
        for record in font_obj['name'].names:
            if b'\x00' in record.string:
                name_str = record.string.decode('utf-16-be')
            else:
                name_str = record
            if record.nameID == self.FONT_SPECIFIER_NAME_ID and not name:
                name = name_str
            elif record.nameID == self.FONT_SPECIFIER_FAMILY_ID and not family:
                family = name_str
            if name and family:
                break
        return str(name), str(family)

    def get_font_list_in_directory(self, source_dir_path):
        """
        Description: get list of all font present in a directory
        Input: source_dir_path => srt
        Return: fonts_name_list => list
        """
        fonts_name_list = []
        # get list of files in directory
        _, _, files_list = next(os.walk(source_dir_path))
        # check if any font present in list
        for file_name in files_list:
            for post_fix in self.fonts_post_fix:
                if file_name.endswith(post_fix):
                    fonts_name_list.append(file_name)
        # return fonts list
        return fonts_name_list

    @staticmethod
    def get_installed_fonts():
        """
        Description: get installed font by run fc-list shell commend
        Return: out => str
        """
        p = subprocess.Popen('fc-list', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return str(out)

    def install_fonts(self, fonts_name_list, source_dir_path, force_install=False):
        """
        Description: copy fonts to share folder and rebuild font cache
        Input: fonts_name_list => list, source_dir_path => str
        """
        # if font list empty return
        if not fonts_name_list:
            print(colored('there is no font for installation', 'red'))
            return False
        installed_fonts = self.get_installed_fonts()
        current_install_count = 0
        for font_name in fonts_name_list:
            source_path = f'{source_dir_path}/{font_name}'
            destination_path = f'{self.DESTINATION_FONTS_PATH}/{font_name}'
            ttf_name, ttf_family = self.ttf_obj_to_name(ttLib.TTFont(source_path))

            if not os.path.exists(destination_path) and \
                    (ttf_name not in installed_fonts or ttf_family not in installed_fonts) or \
                    force_install:
                shutil.copyfile(source_path, destination_path)
                current_install_count += 1
                if force_install:
                    print(
                        '{font_name}: {massage}'.format(font_name=font_name, massage=colored('reinstalled', 'magenta')))
                else:
                    print('{font_name}: {massage}'.format(font_name=font_name, massage=colored('installed', 'green')))
            else:
                print('{font_name}: {massage}'.format(font_name=font_name,
                                                      massage=colored('already exist', 'yellow')))

        if current_install_count:
            print(colored('copying done!', 'blue'))
            print(colored('rebuild font cache', 'cyan'))
            subprocess.Popen('fc-list', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(colored('all done!', 'green'))


if __name__ == "__main__":
    font_installer = FontInstaller()
    force_install = False
    install = True
    path = font_installer.CURRENT_PATH

    if '-h' in sys.argv or '--help' in sys.argv:
        print("Install all fonts in a directory with one command\n\n"
              f"{colored('-f, --force', 'cyan')}             reinstall font if already exist like 'font-installer -f'\n"
              f"{colored('-p, --path', 'cyan')}              custom path (default is current path) like 'font-installer -p /opt/fonts/...'\n"
              f"{colored('--create-nemo-action', 'cyan')}    if you use nemo file manager, run this for adding install action"
              " to right click menu\n"
              f"{colored('-w, --wait', 'cyan')}              need enter for exit after program finished\n"
              f"{colored('-h, --help ', 'cyan')}             show help")
        install = False
    elif '--create-nemo-action' in sys.argv:
        # if using linux mint file manager or 'nemo' file manager you can add action to
        # right click menu in 'nemo' (see screenshot)
        action_file = open('font-installer.nemo_action', 'r')
        action_file = action_file.read()
        action_file = action_file.replace('$%path_to_font_installer%$', os.path.realpath(__file__))
        f = open('{home_path}/.local/share/nemo/actions/font-installer.nemo_action'.format(
            home_path=os.path.expanduser("~")), 'w')
        f.write(action_file)
        f.close()
        print(colored('created', 'green'))
        install = False
    elif '-p' in sys.argv or '--path' in sys.argv:
        if '-p' in sys.argv:
            index = sys.argv.index('-p')
        else:
            index = sys.argv.index('--path')
        if len(sys.argv) > index + 1:
            path = sys.argv[index + 1]
        else:
            print(colored('please read help: $ font-installer --help or -h', 'red'))
            install = False
    if '-f' in sys.argv or '--force' in sys.argv:
        force_install = True

    if install:
        fonts_list = font_installer.get_font_list_in_directory(path)
        font_installer.install_fonts(fonts_list, path, force_install=force_install)

    if '-w' in sys.argv or '--wait' in sys.argv:
        input('\npress Enter to exit: ')
