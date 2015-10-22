# Found on the ZshWiki
#  http://zshwiki.org/home/config/prompt
#

CRUNCH_BRACKET_COLOR="%{$fg[white]%}"
CRUNCH_TIME_COLOR="%{$fg[yellow]%}"
CRUNCH_RVM_COLOR="%{$fg[magenta]%}"
CRUNCH_DIR_COLOR="%{$fg[cyan]%}"
CRUNCH_GIT_BRANCH_COLOR="%{$fg[green]%}"
CRUNCH_GIT_CLEAN_COLOR="%{$fg[green]%}"
CRUNCH_GIT_DIRTY_COLOR="%{$fg[red]%}"

# local time, color coded by last return code
time_enabled="%(?.%{$fg[green]%}.%{$fg[red]%})%*%{$reset_color%}"
time_disabled="%{$fg[green]%}%*%{$reset_color%}"
time=$time_enabled

local git_branch='$(git_prompt_info)%{$reset_color%}'

# PROMPT="${git_branch} ${time}%{$fg[green]%} $%{$reset_color%}"
PROMPT="${git_branch}${time_enabled} %(?.%{$fg[green]%}.%{$fg[red]%})%%%{$reset_color%} "

ZSH_THEME_GIT_PROMPT_PREFIX="%(?.%{$fg[green]%}.%{$fg[red]%})|"
ZSH_THEME_GIT_PROMPT_SUFFIX="%(?.%{$fg[green]%}.%{$fg[red]%})|%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[green]%}%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[green]%}"
