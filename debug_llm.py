#!/usr/bin/env python
from dotenv import dotenv_values
from pathlib import Path
import os

env_path = Path(__file__).parent.parent / ".env"
print(f"env_path: {env_path}")
print(f"env_path.exists(): {env_path.exists()}")

if env_path.exists():
    print("File exists, attempting to read...")
    env_vars = dotenv_values(dotenv_path=env_path)
    print(f"env_vars type: {type(env_vars)}")
    print(f"env_vars: {env_vars}")
    print(f"env_vars items: {list(env_vars.items())}")
    
    for key, value in env_vars.items():
        print(f"Setting {key} = {value[:20]}...")
        os.environ[key] = value
    
    print(f"\nAfter setting:")
    print(f"os.getenv('HUGGINGFACE_API_KEY'): {os.getenv('HUGGINGFACE_API_KEY')}")
else:
    print("File does NOT exist!")
