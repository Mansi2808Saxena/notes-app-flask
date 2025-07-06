from flask import Flask, request, redirect, url_for,render_template
from pymongo import MongoClient
from datetime import datetime,timezone

app = Flask(__name__)

client = MongoClient("mongodb+srv://mansisaxena2004:rDZZQ61wLbzpxjpQ@cluster0.4notrqr.mongodb.net/?retryWrites=true&w=majority")
db = client['notes_db']  
notes_collection = db['notes']  

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/notes')
def view_notes():
    notes_cursor = notes_collection.find()
    notes = []
    for note in notes_cursor:
        created_at = note.get('created_at')
        if created_at:
            # If exists, format
            formatted = created_at.strftime('%#d %B %Y, %I:%M %p')
        else:
            # If missing, fallback
            formatted = 'N/A'
        note['formatted_date'] = formatted
        notes.append(note)
    return render_template('view_notes.html', notes=notes)

@app.route('/add',methods=['GET','POST'])
def add_note():
    if request.method == 'POST':
        note_text = request.form['note']
        notes_collection.insert_one({
            'text': note_text,
            'created_at': datetime.now()
            })
        return redirect(url_for('view_notes'))
    return render_template('add_notes.html')

if __name__ == '__main__':
    app.run(debug=True)
