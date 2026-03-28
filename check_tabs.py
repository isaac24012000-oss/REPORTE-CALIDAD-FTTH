with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[693:696], start=694):
        print(f"Línea {i}: {repr(line)}")
