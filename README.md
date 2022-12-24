# FLAC-Check-And-Fix
Checks for corrupted FLAC files in a directory and attempts to fix them by Decoding and Encoding again.

# Usage

Just use `python flac-fix [arguments]`

positional arguments:
  flac_dir         Flac directory path

options:
  -h, --help       show this help message and exit
  --quiet, -q      No output in between?
  --recursive, -r  Check subfolders as well?
  --fix            Try to fix the corrupted files?
  
  For example,
  
  if we want to scan the folder '~/Downloads/music` recursively : 
  
  `flac_dir "~/Downloads/music"`
  
  This will list all corrupted files
  
  Now, we can also try to fix these files by decoding->encoding again by giving `--fix` argument
  
  `flac_dir --fix "~/Downloads/music"`
  
  And if we want to search all subfolders, give the -r argument as well
  
  `flac_dir -r --fix "~/Downloads/music"`
