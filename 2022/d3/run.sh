#!/usr/bin/env sh

# Runs deno at src/d3_deno.ts with arguments ["example.txt"]
echo "example.txt"
deno run --allow-read src/d3_deno.ts "example.txt"

echo "submission.txt"
deno run --allow-read src/d3_deno.ts "submission.txt"


