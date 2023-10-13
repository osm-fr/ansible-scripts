colorscheme elflord
syn on
set ruler
set noai
set title

set is     " incremental search
set hlsearch

set foldlevel=500

" Pour se souvenir de la dernière position dans le fichier
autocmd BufReadPost *
  \ if line("'\"") > 0 && line("'\"") <= line("$") |
  \   exe "normal g`\"" |
  \ endif
