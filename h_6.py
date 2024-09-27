import sqlite3
import random

conn = sqlite3.connect('school_of_magic.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS wizards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        age INTEGER,
        house VARCHAR(20),
        magic_level INTEGER,
        special_ability VARCHAR(50)
    )
''')
conn.commit()

def add_wizard(first_name, last_name, age, house, magic_level, special_ability):
    cursor.execute('''
        INSERT INTO wizards (first_name, last_name, age, house, magic_level, special_ability)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, age, house, magic_level, special_ability))
    conn.commit()

def find_wizard_by_ability(ability):
    cursor.execute('''
        SELECT * FROM wizards WHERE special_ability = ?
    ''', (ability,))
    return cursor.fetchall()

def list_wizards_by_house(house):
    cursor.execute('''
        SELECT * FROM wizards WHERE house = ?
    ''', (house,))
    return cursor.fetchall()

def update_magic_level(wizard_id, new_level):
    cursor.execute('''
        UPDATE wizards SET magic_level = ? WHERE id = ?
    ''', (new_level, wizard_id))
    conn.commit()

def delete_wizard(wizard_id):
    cursor.execute('''
        DELETE FROM wizards WHERE id = ?
    ''', (wizard_id,))
    conn.commit()

def wizard_duel():
    cursor.execute('SELECT * FROM wizards ORDER BY RANDOM() LIMIT 2')
    wizards = cursor.fetchall()

    if len(wizards) == 2:
        wizard1, wizard2 = wizards
        print(f"Дуэль между {wizard1[1]} {wizard1[2]} и {wizard2[1]} {wizard2[2]}!")

        if wizard1[5] > wizard2[5]:
            print(f"{wizard1[1]} выигрывает!")
            update_magic_level(wizard1[0], wizard1[5] + 5)
            update_magic_level(wizard2[0], wizard2[5] - 10)
        elif wizard1[5] < wizard2[5]:
            print(f"{wizard2[1]} выигрывает!")
            update_magic_level(wizard2[0], wizard2[5] + 5)
            update_magic_level(wizard1[0], wizard1[5] - 10)
        else:
            print("Ничья!")

add_wizard('Гарри', 'Поттер', 15, 'Гриффиндор', 90, 'говорить с змеями')
add_wizard('Гермиона', 'Грейнджер', 15, 'Гриффиндор', 95, 'выдающийся ум')
add_wizard('Драко', 'Малфой', 16, 'Слизерин', 85, 'летать на метле')

print(find_wizard_by_ability('летать на метле'))
print(list_wizards_by_house('Гриффиндор'))

update_magic_level(1, 95)
delete_wizard(3)

wizard_duel()

conn.close()