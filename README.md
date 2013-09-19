Clean library
=============

Library cleaner for my torrent directory (shhhhhhhhh). The arborescence is tidying up in another directory, currently, it just makes links to the targeted file, in order to avoid duplication and fill HDD space.

## Initialization

Populate clean.properties with the pathes you want to resolve. The path are created by the script, so do not worry about that.

## Usage

In order to run the cleaner you just have to chmod +x the file runner.sh and execute it. Two behaviour are performed :

* global 

	If no argument is given, the runner will parse all files in DATA_TORRENT_DIR and add them to the END_POINT directory according to the specified types of files encountered.

* specific

	You can pass a directory as an argument. The script will just add it to the END_POINT, and that is all.

## The change file

If the library is messing some directories up you can correct that, the change.sh file is called at the end of the global behaviour. It is a simple bash script, so add your corrections in it (move, rename) in case of a reset.
