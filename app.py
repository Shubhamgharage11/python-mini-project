from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "library_management_secret_key"

JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.json")


def load_books():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_books():
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)


books = load_books()


@app.route("/")
def index():
    total_books = len(books)
    available_books = sum(1 for book in books if book.get("status") == "Available")
    issued_books = sum(1 for book in books if book.get("status") == "Issued")
    return render_template("index.html", books=books, total_books=total_books,
                           available_books=available_books, issued_books=issued_books)


@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book_id = request.form.get("book_id", "").strip()
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        if not book_id or not title or not author:
            flash("Please fill in all the fields.", "error")
            return redirect(url_for("add_book"))
        if any(str(book.get("id")) == book_id for book in books):
            flash("This Book ID already exists.", "error")
            return redirect(url_for("add_book"))
        books.append({"id": book_id, "title": title, "author": author,
                      "status": "Available", "issued_to": ""})
        save_books()
        flash("Book added successfully!", "success")
        return redirect(url_for("index"))
    return render_template("add_book.html")


@app.route("/search", methods=["GET", "POST"])
def search_book():
    results = []
    if request.method == "POST":
        book_id = request.form.get("book_id", "").strip()
        results = [book for book in books if str(book.get("id")) == book_id]
        if not results:
            flash("No book found with this Book ID.", "error")
    return render_template("search.html", results=results)


@app.route("/issue", methods=["GET", "POST"])
def issue_book():
    if request.method == "POST":
        book_id = request.form.get("book_id", "").strip()
        student_name = request.form.get("student_name", "").strip()
        if not book_id or not student_name:
            flash("Please enter the Book ID and student name.", "error")
            return redirect(url_for("issue_book"))
        for book in books:
            if str(book.get("id")) == book_id:
                if book.get("status") == "Issued":
                    flash("This book is already issued.", "error")
                    return redirect(url_for("issue_book"))
                book["status"] = "Issued"
                book["issued_to"] = student_name
                save_books()
                flash("Book issued successfully!", "success")
                return redirect(url_for("index"))
        flash("Book ID not found.", "error")
        return redirect(url_for("issue_book"))
    return render_template("issue_book.html")


@app.route("/return/<book_id>", methods=["POST"])
def return_book(book_id):
    for book in books:
        if str(book.get("id")) == book_id:
            if book.get("status") == "Available":
                flash("This book is already available.", "error")
            else:
                book["status"] = "Available"
                book["issued_to"] = ""
                save_books()
                flash("Book returned successfully!", "success")
            return redirect(url_for("index"))
    flash("Book ID not found.", "error")
    return redirect(url_for("index"))


@app.route("/delete/<book_id>", methods=["POST"])
def delete_book(book_id):
    for book in books:
        if str(book.get("id")) == book_id:
            books.remove(book)
            save_books()
            flash("Book deleted successfully!", "success")
            return redirect(url_for("index"))
    flash("Book ID not found.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
