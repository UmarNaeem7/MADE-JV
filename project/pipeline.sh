# Check if the virtual environment exists
if [ -d "project_venv" ]; then
    echo "Virtual environment already exists. Activating..."
    # Activate the virtual environment depending on the OS
    if [[ "$OSTYPE" == "msys" ]]; then
        source project_venv/Scripts/activate  # For Windows (MSYS, Git Bash)
    else
        source project_venv/bin/activate  # For Linux/macOS
    fi
else
    echo "Virtual environment not found. Creating a new one..."
    # Create a new virtual environment
    python -m venv project_venv
    # Activate the new virtual environment depending on the OS
    if [[ "$OSTYPE" == "msys" ]]; then
        source project_venv/Scripts/activate  # For Windows (MSYS, Git Bash)
    else
        source project_venv/bin/activate  # For Linux/macOS
    fi
fi

# Install dependencies from the requirements.txt file
pip install -r requirements.txt

# Run the data extraction script
python data_extraction.py
