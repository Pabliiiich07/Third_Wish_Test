#!/bin/bash

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Virtual environment already exists."
    source venv/Scripts/activate # Windows
    # source venv/bin/activate # Ubuntu
fi

echo "Running process_problems.py..."
python process_problems.py --strategy rephrase
