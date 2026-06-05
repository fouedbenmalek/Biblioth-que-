import sqlite3

DB_PATH = 'db.sqlite3'

categories = [
    (1, 'Roman'),
    (2, 'Fantastique'),
    (3, 'Classique'),
    (4, 'Science'),
    (5, 'Policier'),
    (6, 'Philosophie'),
    (7, 'Histoire'),
]

rows = [
    ('Le Petit Prince', 'Antoine de Saint-Exupéry', 1, 1943, 5, 'disponible'),
    ("L'Étranger", 'Albert Camus', 1, 1942, 3, 'disponible'),
    ('Les Misérables', 'Victor Hugo', 1, 1862, 4, 'disponible'),
    ("Harry Potter à l'école des sorciers", 'J.K. Rowling', 2, 1997, 7, 'disponible'),
    ('Le Seigneur des Anneaux', 'J.R.R. Tolkien', 2, 1954, 2, 'disponible'),
    ('Candide', 'Voltaire', 3, 1759, 6, 'disponible'),
    ('Sapiens', 'Yuval Noah Harari', 4, 2011, 4, 'disponible'),
    ("L'Alchimiste", 'Paulo Coelho', 1, 1988, 8, 'disponible'),
    ('Da Vinci Code', 'Dan Brown', 5, 2003, 5, 'disponible'),
    ('Le Rouge et le Noir', 'Stendhal', 1, 1830, 3, 'disponible'),
    ("Une brève histoire du temps", 'Stephen Hawking', 6, 1988, 2, 'disponible'),
    ('Les Trois Mousquetaires', 'Alexandre Dumas', 7, 1844, 4, 'disponible'),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Ensure categories exist before books are inserted.
cur.execute('select count(*) from library_categorie')
before_categories = cur.fetchone()[0]
for categorie_id, nom in categories:
    cur.execute('select id from library_categorie where id=?', (categorie_id,))
    if cur.fetchone() is None:
        cur.execute(
            'insert into library_categorie (id, nom) values (?, ?)',
            (categorie_id, nom),
        )

cur.execute('select count(*) from library_livre')
before = cur.fetchone()[0]

for titre, auteur, categorie_id, annee_publication, quantite_disponible, statut in rows:
    cur.execute(
        'select 1 from library_livre where titre=? and auteur=?',
        (titre, auteur),
    )
    if cur.fetchone() is None:
        cur.execute(
            '''insert into library_livre
               (titre, auteur, categorie_id, annee_publication, quantite_disponible, statut)
               values (?, ?, ?, ?, ?, ?)''',
            (titre, auteur, categorie_id, annee_publication, quantite_disponible, statut),
        )

conn.commit()
cur.execute('select count(*) from library_livre')
after = cur.fetchone()[0]

print(f'before={before} after={after}')
print(f'categories before={before_categories} now={len(categories)}')

