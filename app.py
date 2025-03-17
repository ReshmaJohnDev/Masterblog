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


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
     This route will remove the specified blog post from our blog_posts list
     and redirect the user back to the home page.
    """
    blog_posts = fetch_blog_post()
    updated_post = [blog_post for blog_post in blog_posts if blog_post['id'] != post_id]
    write_blog_post(updated_post)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    This route will load the update form
    Update the form to send a POST request to the same route, which will then
    update the blog post in our storage.
    """
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Retrieve form data
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Fetch current blog posts
        blog_posts = fetch_blog_post()
        try:
            for i in range(len(blog_posts)):
                if blog_posts[i]['id'] == post['id']:
                    blog_posts[i] = post  # Correctly updates the original list
            write_blog_post(blog_posts)
            return redirect(url_for('index'))
        except Exception as e:
            return render_template('update.html', post=post,
                                  error=f"An error occurred while updating the post: {str(e)}")

    # Render the update form with the current post data
    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)