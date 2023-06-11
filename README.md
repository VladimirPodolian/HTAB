## Local run:

1. Need to create venv from project directory and activate him:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Up server manually:
```bash
./tester.so 127.0.0.1 4000
```

3. Run pytest from the root with the command:
```bash
pytest
```

### Note: 
Run this command in terminal
```bash
export PYTHONPATH="${PYTHONPATH}:/home/path/to/root/folder"
```
If you faced with this issue:
```
ModuleNotFoundError: No module named 'src'
```
