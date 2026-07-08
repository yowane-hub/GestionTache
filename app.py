from flask import Flask, render_template, request, redirect, url_for,session
app = Flask(__name__, template_folder='dossier_html') 
app.secret_key="1b1d7f0061051a0487ed97d85179e76c5df66c24f5461f676bc1b124c1bf9bef"

BASE_DE_DONNE_TACHES ={}
@app.route('/', methods=["GET","POST"])
def accueil():
    if 'utilisateur'not in session: 
        return redirect(url_for('connexion')) 
    utilisateur_actuel=session['utilisateur']
    if request.method=='POST':
        tache_saisie=request.form.get("nom_tache")
        if utilisateur_actuel not in BASE_DE_DONNE_TACHES:
            BASE_DE_DONNE_TACHES[utilisateur_actuel]=[]
        if tache_saisie:
            BASE_DE_DONNE_TACHES[utilisateur_actuel].append(tache_saisie) 
        return redirect(url_for('confirmation', tache=tache_saisie))
    
    mes_taches=BASE_DE_DONNE_TACHES.get(utilisateur_actuel, [])
    return render_template('index.html', prenom=utilisateur_actuel, taches=mes_taches)


@app.route('/connexion', methods=["GET","POST"])
def connexion():
    if 'utilisateur' in session:
        return redirect(url_for('accueil'))

    if request.method=="POST":
        nom=request.form.get('nom_utilisateur')
        mdp=request.form.get('mdp') 

        if nom and mdp:
            if nom=='Yowane' and mdp=='yowane1234':
                session['utilisateur'] = nom
                session['est_admin'] = True 
                return redirect(url_for('admin'))
            else:
                session['utilisateur']=nom 
                session['est_admin'] = False
                return redirect(url_for('accueil')) 
       
    return render_template('connexion.html')
        
@app.route('/deconnexion')
def deconnexion():
    session.pop('utilisateur',None)
    session.pop('est_admin', None)
    return redirect(url_for('connexion'))
    
    return render_template('connexion.html')


@app.route('/confirmation')
def confirmation():
    if 'utilisateur' not in session:
        return redirect(url_for('connexion'))
        
    tache = request.args.get('tache')
    prenom = session['utilisateur'] 
    return render_template('confirmation.html', tache=tache, prenom=prenom)

@app.route('/supprimer/<int:tache_id>')
def supprimer_tache(tache_id):
    if 'utilisateur' in session:
        utilisateur_actuel = session['utilisateur']
        if utilisateur_actuel in BASE_DE_DONNE_TACHES:
            try:
                BASE_DE_DONNE_TACHES[utilisateur_actuel].pop(tache_id)
            except IndexError:
                pass
    return redirect(url_for('accueil'))


@app.route('/admin')
def admin():
    if 'utilisateur' not in session or not session.get('est_admin',False):
        return redirect(url_for('accueil'))
    return render_template('admin.html', toutes_les_donnees=BASE_DE_DONNE_TACHES)

if __name__ == '__main__':   
    app.run(host='127.0.0.1', port=5000, debug=True)