from flask import Flask, request, render_template, redirect, flash

import hackbright

app = Flask(__name__)
app.secret_key="secret stuff"


@app.route("/student")
def get_student():
    """Show information about a student."""

    #github = "jhacks"
    github = request.args.get('github', 'sdevelops')
    first, last, github = hackbright.get_student_by_github(github)
    return render_template("student_info.html", first=first, last=last, github=github)

@app.route("/")
def get_student_form():
    """show form for search a student."""

    return render_template("student_search.html")

@app.route("/create_new")
def get_new_student_form():
    """show form for add a new student."""

    return render_template("create_new_student.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student into the Hackbright database.
    """

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    QUERY = """INSERT INTO students (first_name, last_name, github) VALUES 
    (:first_name, :last_name, :github)"""

    db_cursor = hackbright.db.session.execute(QUERY, {'first_name':first_name,
                                           'last_name':last_name,
                                           'github':github})
    hackbright.db.session.commit()

    flash("Successfully added a student!")

    return redirect("/")

@app.route("/confirmation")
def confirmation_for_new_student():

    return "Successfully created new student."

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
