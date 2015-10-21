set number
syntax on
au WinLeave * set nocursorline nocursorcolumn
au WinEnter * set cursorline cursorcolumn
set cursorline cursorcolumn

set incsearch
set ignorecase
set smartcase
set showmatch
set showcmd

set smartindent
set autoindent
set tabstop=2
set shiftwidth=2
set expandtab
set ruler

color desert

" For error shift
:command W w
:command Wq wq
:command WQ wq
:command Q q
:command Qa qa
:command QA qa

set nobackup
