#!/bin/bash

dir="/home/brilja/Desktop/VChatGPT/tmp/fifos"
p_dir="/home/brilja/Desktop/VChatGPT/tmp/processing"
max_concurrent_processes=15  # Maximum number of concurrent piper processes
declare -A pid_list  # Associative array to keep track of running processes

while :; do
    readarray -t fifo_files < <(find "$dir" -maxdepth 1 -type f)  # Find files in the directory

    for fifo_file in "${fifo_files[@]}"; do
        if [ ${#pid_list[@]} -lt $max_concurrent_processes ]; then
            padded_number=$(echo "$fifo_file" | awk -F '_-_' '{print $2}')

            output_file="/home/brilja/Desktop/VChatGPT/tmp/wavs/${padded_number}.wav"

            # Read FIFO file content into a variable
            fifo_content=$(cat "$fifo_file")

            # Start Piper process in the background with FIFO content
            echo "$fifo_content" | /home/brilja/piper2/piper/piper --model /home/brilja/piper2/amy/en_US-amy-medium.onnx --output_file "$output_file" &
            PID=$!
            pid_list[$PID]=$output_file  # Map PID to its output file

            # Delete the FIFO file
            rm "$fifo_file"
        fi
    done

    # Check and clean up completed processes
    for pid in "${!pid_list[@]}"; do
        if ! kill -0 $pid 2>/dev/null; then  # Check if process is no longer running
            #rm "${pid_list[$pid]}"  # Delete the corresponding FIFO file
            unset pid_list[$pid]  # Remove PID from the list
        fi
    done

    sleep 0.1  # Small delay before restarting loop
done


# #!/bin/bash

# counter=0
# dir="/home/brilja/Desktop/VChatGPT/tmp/fifos"

# while :; do
#     for fifo_file in $dir/*; do
#         next_numb=$(printf "%04d" $counter)
#         # Start cat and Piper process
#         { cat "$fifo_file" | /home/brilja/piper2/piper/piper --model /home/brilja/piper2/amy/en_US-amy-medium.onnx --output_file /home/brilja/Desktop/VChatGPT/tmp/wavs/heyo${next_numb}.wav; } &

#         # Capture the PID of the process
#         PID=$!

#         # Wait for the process to finish
#         wait $PID

#         # if [ -z "$(ls -A $dir)" ]; then
#         #     continue #exit the loop
#         # fi 

#         # Increment the counter
#         ((counter++))
        
#         # delete the file
#         rm "$fifo_file"

#     done
#     # Optionally, add a small delay before restarting
#     sleep 0.1
# done
