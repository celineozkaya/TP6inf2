import sqlite3

connexion = sqlite3.connect("alesc.sqlite")
curseur = connexion.cursor()
r1 = "CREATE TABLE IF NOT EXISTS etudiant (id_etu INTEGER, nom TEXT, prenom TEXT, semestre TEXT)"
#curseur.execute(r1)

r2 = "CREATE TABLE IF NOT EXISTS logement (id_logement INTEGER, type TEXT, label INTEGER)"
#curseur.execute(r2)

r3 = "CREATE TABLE IF NOT EXISTS logeur (id_logeur INTEGER, nom TEXT, prenom TEXT)"
#curseur.execute(r3)

