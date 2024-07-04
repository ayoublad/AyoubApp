from flask import Flask, request, render_template_string, redirect, url_for, session # type: ignore
import random

# Initialize the Flask application
application = Flask(__name__)
application.secret_key = 'supersecretkey'  # Needed to use sessions

# HTML templates
welcome_template = '''
<html>
<head>
    <title>eu du nombre mystere</title>
</head>
<body>
    <h1>Bienvenue {{name}} !</h1>
    <h2>Prêt à deviner le nombre mystère !</h2>
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
            <h1>Bonjour cher employé de Capgemini</h1>
            <h2>Entrez votre prénom pour commencer le jeu:</h2>
            <form method="post">
                <label for="name">Prénom:</label>
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
        
        if session['attempts'] == 5:
            message += f" Qu'est-ce qu'il se passe {session['name']} ? C'est plus difficile que prévu ?"
        
        if session['attempts'] == 9:
            message += f" La seule chose qu'on pourra dire, c'est que {session['name']} a fait preuve de perseverance."

        if session['attempts'] >= 10:
            return render_template_string(result_template, result="Perdu! Vous avez épuisé toutes vos tentatives.", number=session['number'], attempts=session['attempts'])

        return render_template_string(welcome_template, name=session['name'], message=message)

    return render_template_string(welcome_template, name=session['name'], message="")

if __name__ == "__main__":
    application.run()
