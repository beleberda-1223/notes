from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QMessageBox, QGroupBox, QTextEdit, QLineEdit, QListWidget, QInputDialog
import json


notes = {'Добро пожаловать!' : {
'текст' : 'Это самое лучшее приложение для заметок в мире!', 
'тег' : ['инструкция', 'добро']
}}
with open('notes_data.json', 'w') as file:
    json.dump(notes, file)
app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Умные заметки')
main_win.resize(900, 600)

note = QTextEdit()
note_list = QListWidget()
note_list_L = QLabel('Список заметок')
create_note_button = QPushButton('Создать заметку')
delete_note_button = QPushButton('Удалить заметку')
save_note_button = QPushButton('Сохранить заметку')
tags_list_L = QLabel('Список тегов')
enter_tag = QLineEdit('')
enter_tag.setPlaceholderText('Введите тег...')
add_tag_button = QPushButton('Добавить к заметке')
tags_list = QListWidget()
delete_tag_button = QPushButton('Открепить от заметки')
seacrh_note_button = QPushButton('Искать заметки по тегу')


main_layout = QHBoxLayout()
note_layout = QVBoxLayout()
settings_layout = QVBoxLayout()

note_list_H = QHBoxLayout()
tags_list_H = QHBoxLayout()

note_layout.addWidget(note)

note_list_H.addWidget(create_note_button)
note_list_H.addWidget(delete_note_button)
tags_list_H.addWidget(add_tag_button)
tags_list_H.addWidget(delete_tag_button)
settings_layout.addWidget(note_list_L)
settings_layout.addWidget(note_list)
settings_layout.addLayout(note_list_H)
settings_layout.addWidget(save_note_button)
settings_layout.addWidget(tags_list_L)
settings_layout.addWidget(tags_list)
settings_layout.addWidget(enter_tag)
settings_layout.addLayout(tags_list_H)
settings_layout.addWidget(seacrh_note_button)

main_layout.addLayout(note_layout)
main_layout.addLayout(settings_layout)
main_win.setLayout(main_layout)


def show_results():
    name = note_list.selectedItems()[0].text()
    print(name)
    note.setText(notes[name]['текст'])
    tags_list.clear()
    tags_list.addItems(notes[name]['тег'])

note_list.itemClicked.connect(show_results)

def add_note():
    note_name, ok = QInputDialog.getText(main_win, 'Добавить заметку', 'Название заметки')
    if note_name and ok != '':
        notes[note_name] = {'текст' : '', 'тег' : []}
        note_list.addItem(note_name)
        with open('notes_data.json', 'w', encoding = 'UTF-8') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False, indent = 2)
        print(notes)

def del_note():
        if note_list.selectedItems():
            name = note_list.selectedItems()[0].text()
            del notes[name]
            note_list.clear()
            tags_list.clear()
            note.clear()
            note_list.addItems(notes)
            with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys = True, ensure_ascii = False, indent = 2)
            print(notes)
        else:
            print('Заметка не выбрана')

def save_note():
    if note_list.selectedItems():
            name = note_list.selectedItems()[0].text()
            notes[name]['текст'] = note.toPlainText()
            with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys = True, ensure_ascii = False, indent = 2)
            print(notes)
    else:
        print('Заметка не выбрана')

def add_tag():
    if note_list.selectedItems():
            key = note_list.selectedItems()[0].text()
            tag = enter_tag.text()
            if not tag in notes[key]['тег']:
                notes[key]['тег'].append(tag)
                tags_list.addItem(tag)
                enter_tag.clear()
            with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys = True, ensure_ascii = False, indent = 2)
    else:
        print('Заметка для добавления тега не выбрана!')

def delete_tag():
    if tags_list.selectedItems():
        name = note_list.selectedItems()[0].text()
        tag_name = tags_list.selectedItems()[0].text()
        notes[name]['тег'].remove(tag_name)
        tags_list.clear()
        tags_list.addItems(notes[name]['тег'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False, indent = 2)
    else:
        print('Тег не выбран!')

def seacrh_note():
    tag = enter_tag.text()
    if seacrh_note_button.text() == 'Искать заметки по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['тег']:
                notes_filtered[note] = notes[note]
        seacrh_note_button.setText('Сбросить поиск')
        note_list.clear()
        tags_list.clear()
        note_list.addItems(list(notes_filtered.keys()))
    elif seacrh_note_button.text() == 'Сбросить поиск':
        enter_tag.clear()
        note_list.clear()
        tags_list.clear()
        note_list.addItems(list(notes.keys()))
        seacrh_note_button.setText('Искать заметки по тегу')
    else:
        pass
    

create_note_button.clicked.connect(add_note)
delete_note_button.clicked.connect(del_note)
save_note_button.clicked.connect(save_note)
add_tag_button.clicked.connect(add_tag)
delete_tag_button.clicked.connect(delete_tag)
seacrh_note_button.clicked.connect(seacrh_note)

main_win.show()
with open('notes_data.json', 'r') as file:
    load = json.load(file)
notes = load
note_list.addItems(list(notes.keys()))
app.exec_()