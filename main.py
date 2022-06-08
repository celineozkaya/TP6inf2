import sqlite3
import pandas as pd

#Partie 1

connexion = sqlite3.connect("alesc.sqlite")
curseur = connexion.cursor()
r1 = "CREATE TABLE IF NOT EXISTS etudiant (id_etu INTEGER constraint etudiant_pk primary key autoincrement, id_logement INTEGER references logement,  nom TEXT, prenom TEXT, semestre TEXT)"
curseur.execute(r1)

r2 = "CREATE TABLE IF NOT EXISTS logement (id_logement INTEGER constraint logement_pk primary key autoincrement, type_l TEXT, label INTEGER, numero_rue INTEGER, rue TEXT, code_postal INTEGER, ville TEXT, id_type_logement INTEGER references type_logement, id_logeur INTEGER references logeur, UNIQUE(numero_rue, rue))"
curseur.execute(r2)

r3 = "CREATE TABLE IF NOT EXISTS logeur (id_logeur INTEGER constraint logeur_pk primary key autoincrement, nom TEXT, prenom TEXT, numero_rue INTEGER, rue TEXT, code_postal INTEGER, ville TEXT, UNIQUE(nom, prenom))"
curseur.execute(r3)

r4 = "CREATE TABLE IF NOT EXISTS type_logement (id_type INTEGER constraint type_logement_pk primary key autoincrement, type_l TEXT, UNIQUE(type_l))"
curseur.execute(r4)


#Partie 2
#Remplissage de la table des logeurs
data = pd.read_excel("logeurs.xlsx")
for i in range(len(data)):
    log = (data.nom[i],data.prenom[i],int(data.numero_rue[i]), data.nom_rue[i], int(data.code_postal[i]), data.ville[i])
    curseur.execute(f'INSERT or Ignore INTO logeur(id_logeur, nom, prenom, numero_rue, rue, code_postal, ville) VALUES (NULL, ?, ?, ?, ?, ?, ?)', log)

# Remplissage de la table des logements
data = pd.read_excel("logements.xlsx")

# Remplissage de la table des types
for j in range(len(data)):
    typ = (data.type_logement[j],)
    #print(f' type : {typ}')
    #  r_typ = f'SELECT id_type from type_logement where type_l="{typ}"'
    curseur.execute(f'INSERT or IGNORE INTO type_logement(type_l) VALUES (?)', typ)
   # curseur.execute(f'SELECT id_type from type_logement where type_l="{typ}"')
   # result_typ = curseur.fetchall()
    #print(result_typ)


#les logements
for i in range(len(data)):
    typ = data.type_logement[i]
    print(f' type : {typ}')
  #  r_typ = f'SELECT id_type from type_logement where type_l="{typ}"'
   # curseur.execute(f'INSERT or IGNORE INTO type_logement(type_l) VALUES (?)', typ)
   # print(data.head())
    curseur.execute(f'SELECT id_type from type_logement where type_l="{typ}"')
    result_typ = curseur.fetchall()
    #print(f' resultat id type : {result_typ}')

    logm = (data.type_logement[i], int(data.label[i]), int(data.numero_rue[i]), data.nom_rue[i], int(data.code_postal[i]),
    data.ville[i])

    logeur = (data.nom_logeur[i], data.prenom_logeur[i])
    r_logeur = f'SELECT id_logeur from logeur where nom ="{data.nom_logeur[i]}" AND prenom = "{data.prenom_logeur[i]}"'
    curseur.execute(r_logeur)
    result_logeur = curseur.fetchall()
   # print(f'logeur : {result_logeur}')

    curseur.execute(f'INSERT or Ignore INTO logement(type_l, label, numero_rue, rue, code_postal, ville, id_type_logement, id_logeur) VALUES (?,?, ?, ?, ?,?, {result_typ[0][0]}, {result_logeur[0][0]})',logm)



# Remplissage de la table etudiant
data = pd.read_excel("etudiants.xlsx")
for i in range(len(data)):
    etu = (data.nom[i], data.prenom[i], data.semestre[i])
    r_logement = f'SELECT id_logement from logement where numero_rue = {int(data.numero_rue[i])} and rue= "{data.nom_rue[i]}" and code_postal = {int(data.code_postal[i])} and ville = "{data.ville[i]}"'
    curseur.execute(r_logement)
    result_logement = curseur.fetchall()
    curseur.execute(f'INSERT or Ignore INTO etudiant(id_logement, nom, prenom, semestre) VALUES ({result_logement[0][0]}, ?,?, ?)',etu)


connexion.commit()



https://code-with-me.global.jetbrains.com/nFTeMK2rj9uNHeax3gp9rQ#p=PY&fp=1D562CDE91F22D901B6F61E5E0861134AA6075F306911A1CF0FC2676E5A80297
