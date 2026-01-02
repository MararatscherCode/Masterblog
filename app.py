from flask import Flask, render_template, request, redirect, url_for
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


def save_posts(posts):
    """Save posts list to the JSON storage file."""
    try:
        with DATA_FILE.open('w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)
    except Exception:
        # In production you would log the error; keep silent here for simplicity
        pass


@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        posts = load_posts()
        next_id = max((p.get('id', 0) for p in posts), default=0) + 1
        new_post = {
            "id": next_id,
            "author": author or "Anonymous",
            "title": title or "Untitled",
            "content": content or ""
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete post with the given id and redirect to index."""
    posts = load_posts()
    filtered = [p for p in posts if int(p.get('id', -1)) != int(post_id)]
    # Only save if something changed
    if len(filtered) != len(posts):
        save_posts(filtered)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)