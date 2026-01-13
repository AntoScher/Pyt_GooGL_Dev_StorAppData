from google.cloud import firestore

# get the client
db = firestore.Client()

def document_to_dict(doc):
    """
    Convert a Firestore document to a dictionary.
    """
    if not doc.exists:
        return None
    data = doc.to_dict()
    data['id'] = doc.id
    return data

def read(book_id):
    """
    Return the details for a single book.
    """
    doc_ref = db.collection('books').document(str(book_id))
    return document_to_dict(doc_ref.get())


def create(data):
    """
    Create a new book and return the book details.
    """
    doc_ref = db.collection('books').document()
    doc_ref.set(data)
    return read(doc_ref.id)


def update(data, book_id):
    """
    Update an existing book, and return the updated book's details.
    """
    doc_ref = db.collection('books').document(str(book_id))
    doc_ref.set(data)
    return read(book_id)


def delete(book_id):
    """
    Delete a book in the database.
    """
    db.collection('books').document(str(book_id)).delete()


def list():
    """
    Return a list of all books in the database, sorted by title.
    """
    docs = db.collection('books').order_by('title').stream()
    return [document_to_dict(doc) for doc in docs]