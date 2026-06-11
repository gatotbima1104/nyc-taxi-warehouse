#!/bin/bash

LOG_FILE="logs/pipeline.log"

mkdir -p logs

# overwrite old log
> "$LOG_FILE"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting Pipeline" \
| tee -a "$LOG_FILE"

python -u app.py 2>&1 | tee -a "$LOG_FILE" | grep "^\[INFO\]"

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Pipeline completed successfully" \
    | tee -a "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Pipeline failed" \
    | tee -a "$LOG_FILE"
fi