#!/bin/bash

function stepThroughDir {

	if [ -z $1 ] || [ ! -d $1 ]; then
		echo "Enter a valid directory to unpack";
		exit;
	fi

	for entry in $(ls $1); do
		if [ -d $1"/"$entry ]; then
			echo "###### Searching in Folder " $entry
			stepThroughDir $1"/"$entry ;
		else
			if [[ $entry =~ .*zpaq ]]; then
				echo "###### Extracting file" $1"/"$entry;

				#Extract File
				time zpaq x $1"/"$entry -threads 8;

				#Move extracted File to where it comes from 
				filename=`echo $entry | cut -d \. -f 1`;
				mv $filename $1;

				#Remove Zpaq-Archive
				rm $1"/"$entry;

				echo "###### Finished extraction of file" $1"/"$entry;
			fi
		fi
	done;
}

stepThroughDir $1 ;
