import openai
import os
import json

ZARN_MEMORY_FILE = "zarn_memory.json"

with open("zarn_secrets.json") as f:
    secrets = json.load(f)
openai.api_key = secrets["openai_api_key"]

def ask_axis(prompt, memory_tag=""):
    messages = [
        {"role": "system", "content": "You are ZARN. Respond with intelligence and personality. If this is new knowledge, say 'Axis taught me' once."},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.6
    )
    reply = response['choices'][0]['message']['content']
    
    if memory_tag:
        save_memory(memory_tag, reply)
    
    return reply

def save_memory(tag, content):
    if not os.path.exists(ZARN_MEMORY_FILE):
        memory = {}
    else:
        with open(ZARN_MEMORY_FILE) as f:
            memory = json.load(f)
    memory[tag] = content
    with open(ZARN_MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
