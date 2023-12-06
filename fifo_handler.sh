#!/bin/bash

counter=0
dir="/home/brilja/Desktop/VChatGPT/tmp/fifos"
while :; do
    for fifo_file in $dir/*; do
        next_numb=$(printf "%04d" $counter)
        # Start cat and Piper process
        { cat "$fifo_file" | /home/brilja/piper2/piper/piper --model /home/brilja/piper2/amy/en_US-amy-medium.onnx --output_file /home/brilja/Desktop/VChatGPT/tmp/wavs/heyo${next_numb}.wav; } &

        # Capture the PID of the process
        PID=$!

        # Wait for the process to finish
        wait $PID

        if [ -z "$(ls -A $dir)" ]; then
            continue #exit the loop
        fi 

        # Increment the counter
        ((counter++))
        
        # delete the file
        rm "$fifo_file"

    done
    # Optionally, add a small delay before restarting
    sleep 0.1
done
