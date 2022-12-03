#!/usr/bin/env sh

# Runs deno at src/d3_deno.ts with arguments ["example.txt"]
echo "example.txt"
deno run --allow-read "${PWD}/src/d3_deno.ts" "${PWD}/data/example.txt"
deno run --allow-read "${PWD}/src/d3_deno_concise.ts" "${PWD}/data/example.txt"

echo "submission.txt"
deno run --allow-read "${PWD}/src/d3_deno.ts" "${PWD}/data/submission.txt"
deno run --allow-read "${PWD}/src/d3_deno_concise.ts" "${PWD}/data/submission.txt"

