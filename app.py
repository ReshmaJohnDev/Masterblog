from flask import Flask , render_template, request, redirect, url_for, flash
import json
import os


FILE_NAME = "blog_post.json"

app = Flask(__name__)

def fetch_blog_post():
    """
    This fn reads the storage file and return the file data
    """
    try:
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as blog_obj:
                return json.load(blog_obj)
        else:
            return []  # Return empty list if file doesn't exist
    except json.JSONDecodeError:
        return []


def fetch_post_by_id(post_id):
    """
    This fn reads the storage file and return the data that matches to post_id
    """
    blog_posts = fetch_blog_post()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


def write_blog_post(blog_posts):
    """
    This fn writes data to storage file
    """
    try:
        with open(FILE_NAME, "w") as blog_obj:
            json.dump(blog_posts, blog_obj,indent=4)
    except IOError as e:
        print(f"Error writing to file: {e}")


@app.route('/')
def index():
    """
    This route will display all blog posts.
    """
    blog_posts = fetch_blog_post()
    if not blog_posts:
        error_message = "Error reading blog posts. Please try again later."
        return render_template('index.html', error_message=error_message)
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    This route is used to add new blog post ,update the storage file and
    redirect the user back to the home page.
    """

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        #fetch the data
        blog_posts = fetch_blog_post()
        if not blog_posts:
            error_message = "Error reading blog posts. Please try again later."
            return render_template('add.html', error_message=error_message)

        blog_id = max(post['id'] for post in blog_posts) + 1
        blog_data = {"id": blog_id, "author": author, "title": title, "content": content}
        blog_posts.append(blog_data)
        write_blog_post(blog_posts)

        # redirect to the index
        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)