from flask import Flask, render_template
import json
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path(__file__).resolve().parent / 'posts.json'


def load_posts():
    """Load posts from the JSON storage file. Returns a list of post dicts."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)