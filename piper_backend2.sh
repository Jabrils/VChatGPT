#!/bin/bash

counter=0

while :; do
    # Start cat and Piper process
    { cat /tmp/piper_fifo | /home/brilja/piper2/piper/piper --model /home/brilja/piper2/amy/en_US-amy-medium.onnx --output_file /temp/heyo${counter}.wav; } &

    # Capture the PID of the process
    PID=$!

    # Wait for the process to finish
    wait $PID

    # INSERT COMMUNICATION BACK TO PYTHON SCRIPT
    echo "/temp/heyo${counter}.wav" > /tmp/audio_finished

    # Increment the counter
    ((counter++))
    
    # Optionally, add a small delay before restarting
    sleep 0.1
done
