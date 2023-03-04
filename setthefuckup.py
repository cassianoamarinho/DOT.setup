import os
import json
import shutil
from pathlib import Path
from datetime import datetime
import argparse
from cryptography.fernet import Fernet
from getpass import getpass
import textwrap


#argument setup
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
                                 description=textwrap.dedent('''\
            this is the greatest script in the world.
            ----------------------------------------------
            [install] to setting up the necessary resources on the system;
            [backup] to copy all your dot.files to github repo, ;
            [restore] to restore the dot.files in the root folder of your system; 
            [keygen] to generate an encryption key for the sensive files.
            [status] a git status of files changed.
        '''))
parser.add_argument('command', type=str, help='options: install, restore, backup, keygen or status')
parser.add_argument('-n', '--notlog', action="store_true", help='not show logs')
parser.add_argument('-c', '--cryptofiles', action="store_true", help='enabled the backup of sensive files')
###########################
# to-do # distro argument #
###########################
# parser.add_argument('-d', '--distro', action="store", help='set distro. options: [elementary]')

args = parser.parse_args()

HOME_DIR = str(Path.home())
DOTS_DIR = f'{HOME_DIR}/.dot.setup/dots'
TEMP_DIR = f'{HOME_DIR}/.dot.setup/.tmp'

with open(f'{HOME_DIR}/.dot.setup/conf.json') as f:
    conf = json.load(f)

PYTHON_VERSION = conf.get('python-version')


def logs(message, qtd_idt = 0):
    identation = ''
    while qtd_idt > 0:
        identation = identation + '\t'
        qtd_idt -= 1
    
    if not args.notlog: print(f'{identation}{message}')


def backup():
    logs(f'backup in progress ####')

    for folder in conf.get('folders'): 
        shutil.copytree(f'{HOME_DIR}/{folder}', f'{DOTS_DIR}/{folder}', dirs_exist_ok=True)

        logs(f'the {folder} backup is done!', 1)
        
    for file in conf.get('files'):
        shutil.copy(f'{HOME_DIR}/{file}', f'{DOTS_DIR}/{file}')

        logs(f'the {file} backup is done!', 1)

    if args.cryptofiles:
        fernet = Fernet(str.encode(getpass(prompt='crypto.key: ')))
        for cryptofile in conf.get('cryptofiles'):
            
            # opening the original file to encrypt
            with open(f'{HOME_DIR}/{cryptofile}', 'rb') as file:
                original = file.read()
            
            # encrypting the file
            encrypted = fernet.encrypt(original)
            
            # opening the file in write mode and writing the encrypted data
            filename = f'{TEMP_DIR}/{cryptofile}'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)

            os.makedirs(os.path.dirname(f'{DOTS_DIR}/{cryptofile}'), exist_ok=True)
            shutil.copy(filename, f'{DOTS_DIR}/{cryptofile}')

            shutil.rmtree(f'{TEMP_DIR}')

            logs(f'the {cryptofile} backup is done!', 1)

    logs(f'this stupid backup is fucking done! ####')
    logs(f'####')
    logs(f'start commiting! ####')

    message = f'backup dot files | {datetime.now().strftime("%d-%m-%Y, %H:%M:%S")}'

    logs(f'commit - {message} ####', 1)

    os.system(f"cd ~/.dot.setup ; git add . ; git commit -am '{message}'; git push ; cd")


def restore():
    logs(f'restore in progress ####')

    for folder in conf.get('folders'):
        shutil.copytree(f'{DOTS_DIR}/{folder}', f'{HOME_DIR}/{folder}', dirs_exist_ok=True)

        logs(f'the {folder} restore is done!', 1)

    for file in conf.get('files'):
        shutil.copy(f'{DOTS_DIR}/{file}', f'{HOME_DIR}/{file}')

        logs(f'the {file} restore is done!', 1)
    
    if args.cryptofiles:
        fernet = Fernet(str.encode(getpass(prompt='crypto.key: ')))
        for cryptofile in conf.get('cryptofiles'):
            
            # opening the encrypted file
            with open(f'{DOTS_DIR}/{cryptofile}', 'rb') as enc_file:
                encrypted = enc_file.read()
            
            # decrypting the file
            decrypted = fernet.decrypt(encrypted)
            
            # opening the file in write mode and writing the encrypted data
            filename = f'{TEMP_DIR}/{cryptofile}'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as dec_file:
                dec_file.write(decrypted)

            os.makedirs(os.path.dirname(f'{HOME_DIR}/{cryptofile}'), exist_ok=True)
            shutil.copy(filename, f'{HOME_DIR}/{cryptofile}')

            shutil.rmtree(TEMP_DIR)

            logs(f'the {cryptofile} backup is done!', 1)
    
    logs(f'the dumass dot.setup is fucking restored! ####')
    

def install():
    logs(f'installation in progress ####')

    #set up applications
    os.system("sudo apt update; sudo apt upgrade -y; sudo apt install -y exa bat git tmux tmate zsh vim curl ubuntu-restricted-extras software-properties-common make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev pipenv")
    
    os.system('sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')
    
    os.system(f'mkdir -pv ~/workspace/tools ; cd ~/workspace/tools ; curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"')
    os.system(f"sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl")
    os.system(f"rm kubectl")

    os.system(f'curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-419.0.0-linux-x86_64.tar.gz')
    os.system(f'tar -xf google-cloud-cli-419.0.0-linux-x86_64.tar.gz')
    os.system(f'google-cloud-sdk/install.sh')
    os.system(f'rm google-cloud-cli-419.0.0-linux-x86_64.tar.gz')

    os.system(f'curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3')
    os.system(f'chmod 700 get_helm.sh')
    os.system(f'./get_helm.sh')
    os.system(f'rm get_helm.sh ; cd')

    os.system(f'sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx')
    os.system(f'sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx')
    os.system(f'sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens')

    os.system("curl https://pyenv.run | bash;")

    #syncthing
    os.system("sudo curl -o /usr/share/keyrings/syncthing-archive-keyring.gpg https://syncthing.net/release-key.gpg")
    os.system('echo "deb [signed-by=/usr/share/keyrings/syncthing-archive-keyring.gpg] https://apt.syncthing.net/ syncthing stable" | sudo tee /etc/apt/sources.list.d/syncthing.list')
    os.system("sudo apt update; sudo apt install syncthing")

    os.system(f"pip3 install -r ~/.dot.setup/requirements.txt")
    
    args.cryptofiles = True
    restore()
    
    os.system(f"chmod 600 ~/.ssh/id_rsa")

    os.system(f"exit terminal in 5sec..")
    os.system(f"sleep 5s ; exit")

    #python install with pyenv
    # os.system(f"pyenv install {PYTHON_VERSION}")
    # os.system(f"pyenv global {PYTHON_VERSION}")
    # os.system(f"pyenv local {PYTHON_VERSION}")

    ###########################
    # to-do # terraform setup #
    ###########################
    # https://releases.hashicorp.com/terraform/0.15.0/terraform_0.15.0_linux_amd64.zip
    # cd ~/workspace/tools ; wget https://releases.hashicorp.com/terraform/1.0.7/terraform_1.0.7_linux_amd64.zip
    # unzip terraform_1.0.7_linux_amd64.zip
    # sudo mv terraform /usr/local/bin/
    #
    # https://brain2life.hashnode.dev/how-to-install-tfenv-terraform-version-manager-on-ubuntu-os

    ###########################
    # to-do # distro argument #
    ###########################
    # if args.distro == 'elementary':
    #     # tweaks and ulauncher
    #     os.system("sudo add-apt-repository ppa:philip.scott/pantheon-tweaks")
    #     os.system("sudo add-apt-repository ppa:agornostal/ulauncher")
    #     os.system("sudo apt update; sudo apt install ulauncher pantheon-tweaks")
    #
    #     #configure to show apps in tray
    #     os.system(f"sudo apt-get install libglib2.0-dev libgranite-dev libindicator3-dev libwingpanel-dev indicator-application")
    #     os.system(f"wget -c https://github.com/Lafydev/wingpanel-indicator-ayatana/raw/master/com.github.lafydev.wingpanel-indicator-ayatana_2.0.8_odin.deb")
    #     os.system(f"sudo dpkg -i ./com.github.lafydev.wingpanel*.deb")
    #     os.system(f"mkdir -p ~/.config/autostart; cp /etc/xdg/autostart/indicator-application.desktop ~/.config/autostart/; sed -i 's/^OnlyShowIn.*/OnlyShowIn=Unity;GNOME;Pantheon;/' ~/.config/autostart/indicator-application.desktop;")


def keygen():
    logs(f"get and save this motherfucker crypto.key {str(Fernet.generate_key().decode('UTF-8'))} in any place where you like.")


def status():
    os.system(f"cd ~/.dot.setup ; git status ; cd")


def main():
    opt = { 'backup':backup, 'restore':restore, 'install':install, 'keygen':keygen, 'status':status }

    # try:
    opt.get(args.command)()
    # except:
    #     logs("you choose only this options: install, restore, backup, keygen or status.")
    

if __name__ == '__main__':
    main()