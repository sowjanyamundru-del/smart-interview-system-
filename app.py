from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "smart-interview-123"

# Ikkada nee questions add cheyyi
QUESTIONS = [
    {"q": "Tell me about yourself.", "type": "text"},
    {"q": "What is Python? Explain in 2 lines.", "type": "text"},
    {"q": "What is HTML? What is it used for?", "type": "text"},
    {"q": "What is your biggest strength?", "type": "text"},
    {"q": "Why should we hire you?", "type": "text"},
]

@app.route('/')
def home():
    session['answers'] = []
    session['current'] = 0
    return render_template('index.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    current = session.get('current', 0)

    if request.method == 'POST':
        answer = request.form.get('answer', '')
        answers = session.get('answers', [])
        answers.append(answer)
        session['answers'] = answers
        session['current'] = current + 1
        current = current + 1

        if current >= len(QUESTIONS):
            return redirect(url_for('result'))
        return redirect(url_for('question'))

    if current >= len(QUESTIONS):
        return redirect(url_for('result'))

    q = QUESTIONS[current]
    return render_template('question.html', q=q, num=current+1, total=len(QUESTIONS))

@app.route('/result')
def result():
    answers = session.get('answers', [])
    return render_template('result.html', questions=QUESTIONS, answers=answers)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)