#!/bin/bash

# Function to split input file, process each part, and save the output
process_file() {
  local input_file=$1
  local model_path=$2
  local token_limit=3000

  # Directory for split files
  local split_dir="split_files"
  mkdir -p $split_dir

  # Split the file into sub-files of approximately 3000 tokens each.
  # This uses 'awk' to count tokens based on a whitespace delimiter.
  awk -v RS='[[:space:]]+' -v token_limit="$token_limit" '
  {
    if (token_count > token_limit) {
      file_count++;
      token_count = 0;
    }
    if (token_count == 0) {
      file_name = sprintf("'"$split_dir"'/part_%d.txt", file_count);
    }
    print $0 >> file_name;
    token_count++;
  }' $input_file

  # Directory for output files
  local output_dir="output_files"
  mkdir -p $output_dir

  # Process each split file
  for file in $split_dir/part_*.txt; do
    # Define output file
    local output_file="${file/$split_dir/$output_dir}"

    # Run the command, assume that the processing script reads from stdin and writes to stdout.
    # Filter the output to extract the text between two markers.
    ./main -ngl 32 -m "$model_path" --color -c 4096 --temp 0.7 --repeat_penalty 1.1 --n-predict -1 -p "$(cat $file)" | sed -n '/^/,/\[end of text\]/p' > $output_file
  done
}

# Call the function with specified parameters
# Example usage:
# process_file "path/to/input.txt" "path/to/model/Meta-Llama-3-8B-Instruct-Q3_K_M.gguf"
