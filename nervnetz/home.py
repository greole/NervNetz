from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from nervnetz.auth import login_required
from nervnetz.db import get_db

bp = Blueprint('home', __name__)

def get_target_id(targets, name):
    # TODO consider failure
    # TODO use a dict instead of tuples?
    for row in targets:
        print(row[0], row[1], name)
        if name == row[1]:
            return row[0]


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    db = get_db()

    targets = db.execute(
        'SELECT id, username'
        ' FROM user'
    ).fetchall()

    if request.method == 'POST':

        target_name = request.form['target_id']
        target_id = get_target_id(targets, target_name)
        value = request.form['value']
        error = None

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO relations (author_id, target_id, value)'
                ' VALUES (?, ?, ?)',
                (g.user['id'], target_id, value)
            )
            db.commit()
            return redirect(url_for('home.index'))


    relations = db.execute(
        'SELECT id, author_id, target_id, created, value'
        ' FROM relations '
        ' ORDER BY created DESC'
    ).fetchall()

    usernames = {target[0]: target[1] for target in targets}

    return render_template('home/index.html',
            posts=relations, usernames = usernames, targets=targets)
