from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

# Creating the Model


class BlogPost(db.Model):
    # creating the columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return f'Blog post: {self.title}'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        # collect data
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        # initialise the model
        new_post = BlogPost(
            title=post_title, content=post_content, author=post_author)
        # add data to dbModel
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        # reading from the db
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


# Delete Route
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


# Edit route
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get(id)
    print(post)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit_post.html', posts=post)


@app.route('/home//users/<string:name>/posts/<int:id>')
def hello(name, id):
    return f'Hello {name} your id is {id}'


@app.route('/get', methods=['GET', 'POST'])
def get_req():
    return 'only get this webpage'


if __name__ == '__main__':
    app.run(debug=True)
