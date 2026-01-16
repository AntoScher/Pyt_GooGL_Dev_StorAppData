from flask import Flask, redirect, render_template, request, url_for, current_app
import booksdb
import storage

app = Flask(__name__)
app.config.update(
    SECRET_KEY='secret',
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif']),
)
app.debug = True
app.testing = False

def upload_image_file(img):
    """
    Upload the user-uploaded file to Cloud Storage and retrieve its
    publicly accessible URL.
    """
    if not img:
        return None

    public_url = storage.upload_file(
        img.read(),
        img.filename,
        img.content_type
    )

    current_app.logger.info(
        'Uploaded file %s as %s.', img.filename, public_url)

    return public_url

@app.route('/')
def list():
    books = booksdb.list()
    return render_template('list.html', books=books)

@app.route('/books/<book_id>')
def view(book_id):
    book = booksdb.read(book_id)
    return render_template('view.html', book=book)

@app.route('/books/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        image_url = upload_image_file(request.files.get('image'))

        # If an image was uploaded, update the data to point to the image.
        if image_url:
            data['imageUrl'] = image_url

        book = booksdb.create(data)
        return redirect(url_for('.view', book_id=book['id']))
    return render_template('form.html', action='Add', book={})

@app.route('/books/<book_id>/edit', methods=['GET', 'POST'])
def edit(book_id):
    book = booksdb.read(book_id)
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
 
        image_url = upload_image_file(request.files.get('image'))

        # If an image was uploaded, update the data to point to the image.
        if image_url:
            data['imageUrl'] = image_url
            
        book = booksdb.update(data, book_id)
        return redirect(url_for('.view', book_id=book['id']))
    return render_template('form.html', action='Edit', book=book)

@app.route('/books/<book_id>/delete')
def delete(book_id):
    booksdb.delete(book_id)
    return redirect(url_for('.list'))

# this is only used when running locally
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)