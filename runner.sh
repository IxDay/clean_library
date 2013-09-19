#!/bin/bash

TOP_DIR=$(cd $(dirname "$0") && pwd)
CLEAN_SCRIPT="$TOP_DIR/clean.py"
CHANGE_SCRIPT="$TOP_DIR/change.sh"
PROPERTY_FILE="$TOP_DIR/clean.properties"

if [[ ! -a "$PROPERTY_FILE" ]]; then
	echo "There is no property file, ERROR!"
	exit 1
fi



function trim () {
	echo $(echo "$1" | sed -e 's/^ *//g' -e 's/ *$//g')
}

function check_properties () {	

	[[ -z $DATA_TORRENT_DIR ]] && 
	echo "The variable DATA_TORRENT_DIR was not correctly populate in the property file" && 
	exit 1

	[[ -z $END_DIR ]] && 
	echo "The variable END_DIR was not correctly populate in the property file" && 
	exit 1

	[[ -z $TV_SHOWS_DIR ]] && 
	echo "The variable TV_SHOWS_DIR was not correctly populate in the property file" && 
	exit 1

	[[ -z $MOVIES_DIR ]] && 
	echo "The variable MOVIES_DIR was not correctly populate in the property file" && 
	exit 1

	[[ -z $MUSICS_DIR ]] && 
	echo "The variable MUSICS_DIR was not correctly populate in the property file" && 
	exit 1

	[[ -z $MISC_DIR ]] && 
	echo "The variable MISC_DIR was not correctly populate in the property file" && 
	exit 1
}

function construct_path () {
	export TV_SHOWS_DIR="${END_DIR}/${TV_SHOWS_DIR}"
	export MOVIES_DIR="${END_DIR}/${MOVIES_DIR}"
	export MUSICS_DIR="${END_DIR}/${MUSICS_DIR}"
	export MISC_DIR="${END_DIR}/${MISC_DIR}"	
}

function main () {
	if [[ ! -a "$CLEAN_SCRIPT" ]]; then
		echo "Python script for cleaning up directory was not found"
		exit 1
	fi


	if [[ -z "$1" ]]; then
		python "$CLEAN_SCRIPT"

		if [[ -a "$CHANGE_SCRIPT" ]]; then
			bash "$CHANGE_SCRIPT"
		fi
		exit
	fi

	if [[ ! -a "$1" ]]; then
		echo "File does not exist, ERROR!"
		exit 1
	fi

	python "$CLEAN_SCRIPT" "$1"
}


IFS="="
while read -r NAME VALUE
do
	if [[ ! -z "$NAME" ]]; then
		declare $(trim "$NAME")=$(trim "$VALUE")
	fi
done < "$PROPERTY_FILE"

check_properties
construct_path
main