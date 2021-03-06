import sqlite3
import pandas as pd
from tkinter import *

# Partie 1

connexion = sqlite3.connect("alesc.sqlite")
curseur = connexion.cursor()

# Creation de la table etudiant si elle n'existe pas encore
r1 = "CREATE TABLE IF NOT EXISTS etudiant (id_etu INTEGER constraint etudiant_pk primary key autoincrement, id_logement INTEGER references logement,  nom TEXT, prenom TEXT, semestre TEXT, UNIQUE(nom, prenom))"
curseur.execute(r1)

# Creation de la table logement si elle n'existe pas encore
r2 = "CREATE TABLE IF NOT EXISTS logement (id_logement INTEGER constraint logement_pk primary key autoincrement, type_l TEXT, label INTEGER, numero_rue INTEGER, rue TEXT, code_postal INTEGER, ville TEXT, id_type_logement INTEGER references type_logement, id_logeur INTEGER references logeur, UNIQUE(numero_rue, rue))"
curseur.execute(r2)

# Creation de la table logeur si elle n'existe pas encore
r3 = "CREATE TABLE IF NOT EXISTS logeur (id_logeur INTEGER constraint logeur_pk primary key autoincrement, nom TEXT, prenom TEXT, numero_rue INTEGER, rue TEXT, code_postal INTEGER, ville TEXT, UNIQUE(nom, prenom))"
curseur.execute(r3)

# Creation de la table type si elle n'existe pas encore
r4 = "CREATE TABLE IF NOT EXISTS type_logement (id_type INTEGER constraint type_logement_pk primary key autoincrement, type_l TEXT, UNIQUE(type_l))"
curseur.execute(r4)


# Partie 2

# Remplissage de la table des logeurs
data = pd.read_excel("logeurs.xlsx")
for i in range(len(data)):
    log = (data.nom[i],data.prenom[i],int(data.numero_rue[i]), data.nom_rue[i], int(data.code_postal[i]), data.ville[i])
    curseur.execute(f'INSERT or Ignore INTO logeur(id_logeur, nom, prenom, numero_rue, rue, code_postal, ville) VALUES (NULL, ?, ?, ?, ?, ?, ?)', log)

# Remplissage de la table des logements et des types
data = pd.read_excel("logements.xlsx")

# les types
for j in range(len(data)):
    typ = (data.type_logement[j],)
    # insertion du type dans la table s'il n'a pas encore été ajouté
    curseur.execute(f'INSERT or IGNORE INTO type_logement(type_l) VALUES (?)', typ)

# les logements
for i in range(len(data)):
    typ = data.type_logement[i]
    # on cherche l'id du type du logement
    curseur.execute(f'SELECT id_type from type_logement where type_l="{typ}"')
    result_typ = curseur.fetchall()

    logm = (data.type_logement[i], int(data.label[i]), int(data.numero_rue[i]), data.nom_rue[i], int(data.code_postal[i]),data.ville[i])

    logeur = (data.nom_logeur[i], data.prenom_logeur[i])
    # on cherche l'id du proprietaire
    r_logeur = f'SELECT id_logeur from logeur where nom ="{data.nom_logeur[i]}" AND prenom = "{data.prenom_logeur[i]}"'
    curseur.execute(r_logeur)
    result_logeur = curseur.fetchall()

    # insertion du logement dans la table
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
curseur.close()
connexion.close()




# Partie 3
"""

nom = input("Entrez le nom du logeur : ")
prenom = input("Entrez le prénom du logeur : ")

def resultat_logement(nom, prenom):
    curseur.execute(f"SELECT id_logeur FROM logeur WHERE nom='{nom.lower()}' AND prenom='{prenom.lower()}'")
    id_logr = curseur.fetchall()
    #print(id_logr)
    curseur.execute(f"SELECT type_l, label, numero_rue, rue, code_postal, ville, id_logement FROM logement WHERE id_logeur={id_logr[0][0]}")
    result_logement = curseur.fetchall()
    #print(result_logement)
    print(f"Nom du logeur : {nom} {prenom}")
    i = 0
    for k in result_logement:
        i+=1
        print(f"Logement {i} : {k[2]} rue {k[3]}, {k[4]} {k[5]}, {int(k[1]) * '*'} {k[0]}")
        curseur.execute(f"SELECT nom, prenom FROM etudiant WHERE id_logement={k[6]}")
        result_etudiant = curseur.fetchall()
        for j in result_etudiant:
            print(f"Nom de l'étudiant : {j[0]} {j[1]}")
    return result_logement, result_etudiant
"""

# Partie 3 appli

class Fenetre(Tk):
    def __init__(self, title, height=1000, width=1000):
        # Appel du constructeur de Tk
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")


        self.nom = StringVar()
        self.prenom = StringVar()


        frame = Frame(self)
        frame.grid()  # Placer le frame dans la fenêtre principale
        self.frame2 = Frame(self)
        self.frame2.grid()
        # Ligne 1 -> 'alesc'
        Label(frame, text="ALESC :").grid(column=1, row=0, padx=10, pady=10, columnspan=2, sticky='e')

        # Ligne 2, 3 -> Label 'Nom du logeur' + Entry
        Label(frame, text="Nom du logeur :", bg='yellow').grid(column=0, row=2, padx=10, pady=10, sticky='e')
        Entry(frame, textvariable=self.nom).grid(column=2, row=2, padx=10, pady=10)

        # Ligne 4,5 -> Label 'Prénom du logeur' + Entry
        Label(frame, text="Prénom du logeur :", bg='yellow').grid(column=0, row=3, padx=10, pady=10, sticky='e')
        Entry(frame, textvariable=self.prenom).grid(column=2, row=3, padx=10, pady=10)

        # Bouton valider
        Button(frame, relief=RAISED, borderwidth=10, text="Valider", bg='green', command=lambda : self.requete()).grid(column=2,row=4,padx=10,pady=10)

        #Bouton effacer
        Button(frame, relief=RAISED, borderwidth=10, text="Effacer", bg='green', command=lambda :self.empty()).grid(column=0, row=4, padx=10, pady=10)

        # Bouton quitter
        Button(frame, relief=RAISED, borderwidth=10, text="Quitter", bg='green', command=lambda :self.destroy()).grid(column=1, row=4, padx=10, pady=10)



    # fonction qui efface le contenu de l'ecran
    def empty(self):
        self.prenom.set('')
        self.nom.set('')
        for label in self.frame2.winfo_children():
            label.grid_forget()



    def resultat_logement(self):
        connexion = sqlite3.connect("alesc.sqlite")
        curseur = connexion.cursor()

        for label in self.frame2.winfo_children():
            label.grid_forget()

        nom = self.nom.get()
        prenom = self.prenom.get()

        curseur.execute(f"SELECT id_logeur FROM logeur WHERE nom='{nom.lower()}' AND prenom='{prenom.lower()}'")
        id_logr = curseur.fetchall()
        # print(id_logr)


        curseur.execute(
            f"SELECT type_l, label, numero_rue, rue, code_postal, ville, id_logement FROM logement WHERE id_logeur={id_logr[0][0]}")

        result_logement = curseur.fetchall()
        result_etudiant_total =[]

        if len(result_logement)>0 :
            # print(result_logement)
            print(f"Nom du logeur : {nom} {prenom}")
            i = 0
            for k in result_logement:
                i += 1
                print(f"Logement {i} : {k[2]} rue {k[3]}, {k[4]} {k[5]}, {int(k[1]) * '*'} {k[0]}")
                curseur.execute(f"SELECT nom, prenom FROM etudiant WHERE id_logement={k[6]}")
                result_etudiant = curseur.fetchall()
                result_etudiant_total.append(result_etudiant)

                for j in result_etudiant:
                    print(f"Nom de l'étudiant : {j[0]} {j[1]}")
            connexion.commit()
            curseur.close()
            connexion.close()
            print(result_etudiant)
            print(result_etudiant_total)
            return result_logement, result_etudiant_total
        else :
            return 0,0
    # requete -->  quand on clique sur valider on mets le tableau de resultat de la requete dans self.logement
    def requete(self):

        Label(self.frame2, text=f"Nom du logeur : {self.nom.get()} {self.prenom.get()}").grid(column=0, row=5, padx=10, pady=10, sticky = 'w')
        result_logement, result_etudiant = self.resultat_logement()
        if((result_logement, result_etudiant) != (0,0)):
            i = 1
            for k in result_logement:
                Label(self.frame2, text=f"Logement n°{i}:", bg='red').grid(column=0, row= 6+i*4 , padx=10, pady=10, sticky = 'w')

                Label(self.frame2, text=f"{k[2]} rue {k[3]}, {k[4]} {k[5]}, {int(k[1]) * '*'} {k[0]}").grid(column=0, row=7 + i * 4,padx=10, pady=10, sticky = 'w')


                for j in result_etudiant:
                    for n in range(len(j)):
                        Label(self.frame2, text=f"Nom de l'étudiant : {j[n]} ", bg='white').grid(column=0, row=8+n*4, padx=10, pady=10, sticky = 'w')
                i+=1





        else :
            Label(self.frame2, text=f"Aucun logement n'a été enregistré pour ce logeur").grid(column=0, row=12 , padx=10, pady=10,
                                                                        sticky='w')


if __name__ == "__main__":
    f = Fenetre("TP6")
    f.mainloop()
