#!/bin/bash

# Usage: ./script.sh input_file output_dir [parallelism]
INPUT_FILE="$1"
OUTPUT_DIR="$2"
PARALLEL="${3:-4}"

mkdir -p "$OUTPUT_DIR"

grep -v '^$' "$INPUT_FILE" \
| nl -w1 -s$'\t' \
| xargs -P "$PARALLEL" -n 2 bash -c '
    idx="$0"
    url="$1"
    curl -s "$url" -o "'"$OUTPUT_DIR"'/${idx}_tempdata"
'