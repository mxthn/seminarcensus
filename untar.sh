#!/bin/bash

function stepThroughDir {

	if [ -z $1 ] || [ ! -d $1 ]; then
		echo "Enter a valid directory";
		exit;
	fi

	for entry in $(ls $1); do
		if [ -d $1"/"$entry ]; then
			echo "###### Searching in Folder " $entry
			stepThroughDir $1"/"$entry ;
		else
			if [[ $entry =~ .*tar ]]; then
				echo "###### Extracting file" $1"/"$entry;

				#Extract File
				time tar -xvf $1"/"$entry;

				#Move extracted File to where it comes from and cut off .tar
				filename=`echo $entry | cut -d \. -f 1`;
				mv $filename $1;

				#Remove tar-Archive
				rm $1"/"$entry;

				echo "###### Finished extraction of file" $1"/"$entry;
			fi
		fi
	done;
}

stepThroughDir $1 ;
