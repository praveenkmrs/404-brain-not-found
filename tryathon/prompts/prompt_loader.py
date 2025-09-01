from pathlib import Path

def load_prompt_from_file(prompt_file: str) -> str:
    prompt_path = Path(__file__).parent/prompt_file
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Prompt file not found: {prompt_path}")
        raise
    except Exception as e:
        print(f"Error loading prompt file: {e}")
        raise
