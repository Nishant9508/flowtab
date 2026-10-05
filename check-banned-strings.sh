#!/bin/bash
set -e

BANNED_FILE=".banned-strings"
if [ ! -f "$BANNED_FILE" ]; then
    echo "No .banned-strings file found."
    exit 0
fi

# Build grep args reading lines from .banned-strings, ignoring empty/comment lines
GREP_ARGS=()
while read -r line; do
    # Skip empty lines
    [[ -z "${line}" ]] && continue
    # Skip lines starting with #
    [[ "${line}" == \#* ]] && continue
    GREP_ARGS+=("-e" "${line}")
done < "$BANNED_FILE"

if [ ${#GREP_ARGS[@]} -eq 0 ]; then
    echo "No banned strings configured."
    exit 0
fi

# Search everything except .git directory
echo "Checking for banned strings..."
if git grep -i "${GREP_ARGS[@]}" -- ":^.banned-strings" > .found-banned 2>&1; then
    echo "ERROR: Found banned strings in the following files:"
    cat .found-banned
    rm .found-banned
    exit 1
fi

rm -f .found-banned
echo "Pass: No banned strings found."
exit 0
