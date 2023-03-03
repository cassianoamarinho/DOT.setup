# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="/home/cassiano/.oh-my-zsh"

ZSH_THEME="robbyrussell"

plugins=(git)

source $ZSH/oh-my-zsh.sh

# User configuration

if [ `which tmux 2> /dev/null` -a -z "$TMUX" ]; then
    tmux -2 attach || tmux -2 new; exit
fi

export PATH="$HOME/.pyenv/bin:$PATH"
path+=("$HOME/.local/bin")
export PATH

eval "$(pyenv init --path)"
eval "$(pyenv init -)"

export KUBECONFIG=~/.kube/config
source $HOME/.bash_aliases
export PATH="/usr/local/sbin:$PATH"

export USE_GKE_GCLOUD_AUTH_PLUGIN=True
# The next line updates PATH for the Google Cloud SDK.
if [ -f '/home/cassiano/workspace/tools/google-cloud-sdk/path.zsh.inc' ]; then . '/home/cassiano/workspace/tools/google-cloud-sdk/path.zsh.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/home/cassiano/workspace/tools/google-cloud-sdk/completion.zsh.inc' ]; then . '/home/cassiano/workspace/tools/google-cloud-sdk/completion.zsh.inc'; fi
