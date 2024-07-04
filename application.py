from flask import Flask, request, render_template_string, redirect, url_for, session
import random

# Initialize the Flask application
application = Flask(__name__)
application.secret_key = 'supersecretkey'  # Needed to use sessions

# HTML templates
welcome_template = '''
<html>
<head>
    <title>Bienvenue au jeu du nombre mystere</title>
</head>
<body>
    <h1>Bienvenue au jeu du nombre mystere, {{ name }}!</h1>
    <p>Devinez un nombre entre 1 et 100. Vous avez jusqu'à 10 tentatives.</p>
    <form action="/game" method="post">
        <label for="guess">Entrez un nombre entre 1 et 100:</label>
        <input type="number" id="guess" name="guess">
        <input type="submit" value="Envoyer">
    </form>
    <p>{{ message }}</p>
</body>
</html>
'''

result_template = '''
<html>
<head>
    <title>Résultat</title>
</head>
<body>
    <h1>{{ result }}</h1>
    <p>Le nombre était: {{ number }}</p>
    <p>Vous avez utilisé {{ attempts }} tentatives.</p>
    <a href="/">Recommencer le jeu</a>
</body>
</html>
'''

@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0
        return redirect(url_for('game'))
    return '''
        <html>
        <head>
            <title>Jeu du nombre mystere</title>
        </head>
        <body>
            <h1>Entrez votre prenom pour commencer le jeu:</h1>
            <form method="post">
                <label for="name">Prenom:</label>
                <input type="text" id="name" name="name">
                <input type="submit" value="Commencer le jeu">
            </form>
        </body>
        </html>
    '''

@application.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        guess = int(request.form['guess'])
        session['attempts'] += 1

        if guess < session['number']:
            message = "Trop petit!"
        elif guess > session['number']:
            message = "Trop grand!"
        else:
            return render_template_string(result_template, result="Félicitations! Vous avez deviné le bon nombre.", number=session['number'], attempts=session['attempts'])
        
        if session['attempts'] == 7:
            return render_template_string(result_template, result="Allez {{name}} il te reste encore 3 tentatives", number=session['number'], attempts=session['attempts'])

        if session['attempts'] >= 10:
            return render_template_string(result_template, result="Perdu! Vous avez épuisé vos tentatives.", number=session['number'], attempts=session['attempts'])

        return render_template_string(welcome_template, name=session['name'], message=message)

    return render_template_string(welcome_template, name=session['name'], message="")

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=8000)
