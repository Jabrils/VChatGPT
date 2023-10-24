#!/bin/bash

counter=0

while :; do
    for file_path in /tmp/fifos/*; do
        # Start cat and Piper process
        { cat "$file_path" | /home/brilja/piper2/piper/piper --model /home/brilja/piper2/amy/en_US-amy-medium.onnx --output_file /temp/heyo${counter}.wav; } &

        # Capture the PID of the process
        PID=$!

        # Wait for the process to finish
        wait $PID

        # INSERT COMMUNICATION BACK TO PYTHON SCRIPT
        echo "/temp/heyo${counter}.wav" > /tmp/audio_finished

        # Increment the counter
        ((counter++))
        
    done
    # Optionally, add a small delay before restarting
    sleep 0.1
done