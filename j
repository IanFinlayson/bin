#!/bin/bash

# compile all of them
for f in $*
do
    javac "$f"
done

# find the one with the main function
main=$(grep -lE 'public\s+static\s+void main' $*)

# strip the extension
main=$(echo $main | sed 's/.java$//')

# run it w/o the extension
java $main

