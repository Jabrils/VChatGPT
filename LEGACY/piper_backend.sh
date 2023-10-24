#!/bin/bash

while :; do
    # Start cat and Piper process
    { cat /tmp/piper_fifo | /home/brilja/piper2/piper/piper --model /home/brilja/piper2/amy/en_US-amy-medium.onnx --output-raw | aplay -r 22050 -f S16_LE -t raw -; } &

    # Capture the PID of the process
    PID=$!

    # Wait for the process to finish
    wait $PID

    # INSERT COMMUNICATION BACK TO PYTHON SCRIPT
    touch /tmp/audio_finished
    
    # Optionally, add a small delay before restarting
    sleep 0.1
done
