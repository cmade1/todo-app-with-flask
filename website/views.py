from flask import Blueprint , render_template , request , flash , jsonify , Response ,redirect , url_for
from flask_login import login_required , current_user
from .models import Note
from . import db
import json

views = Blueprint('views' , __name__)

@views.route('/' , methods=['GET' , 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if not note:
            flash('Todo is empty!', category='error')
            return redirect(url_for('views.home'))
        else:
            new_note= Note(data=note , user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Todo Added.' , category='success')
    return render_template("home.html" , user=current_user)
    
@views.route('/delete-note' , methods=['POST'])
def delete_note():
     note = json.loads(request.data)
     noteId= note['noteId']
     note = Note.query.get(noteId)
     if note:
         if note.user_id == current_user.id:
             db.session.delete(note)
             db.session.commit()
             flash('Todo Deleted.' , category='success')
     return jsonify({})

@views.route('/edit/<id>' , methods=['GET' , 'POST']) 
def edit(id):
    note = Note.query.get(id)
    if not note :
        return Response("404 Page Not Found" , 404)
    if request.method == 'POST':
        detail = request.form.get('detail')
        note.data = detail
        db.session.commit()
        flash('Todo Updated!' , category='success')
        return redirect(url_for('views.home'))

    return render_template("home.html" , data=note.data )

