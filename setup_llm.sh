#!/bin/bash

echo "[ZARN LLM] Starting local AI installation..."

Step 1: Install system dependencies

sudo apt update sudo apt install -y cmake g++ git

Step 2: Clone llama.cpp

cd ~ git clone https://github.com/ggerganov/llama.cpp.git cd llama.cpp

Step 3: Build for Raspberry Pi CPU

echo "[ZARN LLM] Compiling llama.cpp (this may take a few minutes)..." make LLAMA_METAL=0 LLAMA_CUBLAS=0

Step 4: Create model folder

mkdir -p models

Step 5: Prompt user to download Mistral 7B Instruct Q4_K_M

cat <<EOM

[ZARN LLM] Build complete!

Next step: Download the model manually (about 4GB):

Go to: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

Download: mistral-7b-instruct.Q4_K_M.gguf

Then move it to: ~/llama.cpp/models/

Example: mv ~/Downloads/mistral-7b-instruct.Q4_K_M.gguf ~/llama.cpp/models/

Once done, run this test: cd ~/llama.cpp ./main -m models/mistral-7b-instruct.Q4_K_M.gguf -p "Who are you?"

EOM

