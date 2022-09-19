from gtts import gTTS  # pip install gtts
import time
from tkinter.filedialog import *
from tkinter import messagebox
from tkinter import *

class auio_start():

    def __init__(self):
        self.words = {}
        self.end_r = 100
        self.start_r = 1
        self.root = Tk()
        self.messagebox = messagebox

    def record_mp3(self, ru, en, path, num):
        if num == 0:
            numbber = ''
        else:
            numbber = str(num) + ' '
        with open(numbber + path + ".mp3", 'wb') as f: #Создали файл в который будем писать звук из текста

            for i in range(0, len(ru)):
                gTTS(ru[i], lang='ru', slow=False).write_to_fp(f) #Записываем в файл озвучку русского текста
                gTTS(en[i], lang='en').write_to_fp(f) #Записываем в файл озвучку английском текста
                gTTS(en[i], lang='en', tld='ca', slow=True).write_to_fp(f)
                gTTS(ru[i], lang='ru', slow=True).write_to_fp(f) #Записываем в файл озвучку русского текста
                gTTS(en[i], lang='en', slow=True).write_to_fp(f) #Записываем в файл озвучку английском текста
                gTTS(en[i], lang='en', tld='ca', slow=False).write_to_fp(f)


    def slovar(self): # подготовка словаря из файла CSV
        self.languages_listbox.delete(0, END)
        try:
            op = askopenfilename(filetypes=[("csv", "*.csv")])
        except:
            return
        spisok = open(op, 'r', encoding='utf-8')
        spisok = spisok.read()

        spisok = spisok.split("\n")
        nummber = 0
        st.words.clear()
        for slovo in range(0, len(spisok)):
            if len(spisok[slovo].split(';')) == 2:
                nummber += 1
                ru = spisok[slovo].split(';')[1]
                en = spisok[slovo].split(';')[0]
                self.words[nummber] = en, ru
                key_word = [k for (k, v) in self.words.items() if v == (self.words[nummber][0], self.words[nummber][1])]
                text_send = '{} {} - {}\n'.format(key_word, self.words[nummber][0], self.words[nummber][1])
                self.languages_listbox.insert(END, text_send)
        print(self.words)

    def dell_word(self): # Удаление слов и списка
        selection = self.languages_listbox.curselection()
        if selection != ():
            numb = self.languages_listbox.get(selection[0]).split(']', 1)[0].lstrip()[1:]
            if numb.rfind(',') > 0:
                numb = numb.split(', ')[-1]
            del st.words[int(numb)]
            self.languages_listbox.delete(selection[0])
        else:
            messagebox.showerror('Ошибка', 'Ошибка: Выберите объект!')

    def add_word(self):
        print('Hello')


    def kolichestvo(self): # Задает назначенное количество слов в фаил
        y = self.end_r
        if len(self.words) != 0:
            try:
                path = asksaveasfilename(filetypes=[("mp3 files", "*.mp3")])
                path = path.split('.mp3')[0]
            except:
                return
            en = []
            ru = []
            for i in range(self.start_r, len(self.words) + 1):
                if self.words.get(i) != None:
                    e, r = self.words.get(i)
                    if i < y:
                        en.append(e)
                        ru.append(r)
                    else:
                        en.append(e)
                        ru.append(r)
                        self.record_mp3(ru, en, path, y)
                        time.sleep(10)
                        y += self.end_r
                        en.clear()
                        ru.clear()
            if len(en) != 0:
                self.record_mp3(ru, en, path, 0)


    def allbind(self, event): # назначение кнопак
        keysym = str(event).split('keysym=', 1)[1].split(' keycode=', 1)[0]
        print(keysym)
        if keysym == 'Delete':
            st.dell_word()
        if keysym == 'Return':
            st.slovar()

    def menu(self): # Основное мнею TK inter
        self.root.title('Создание словаря')
        self.add_button = Button(text="Добавить Словарь", command=self.slovar).grid(column=0, row=0,
                                                                                    sticky=W + E, padx=5, pady=5)
        self.dellet_button = Button(text="Удалить из списка", command=self.dell_word).grid(column=0, row=2,
                                                                                           sticky=W + E, padx=5, pady=5)
        self.addWord_button = Button(text="Добавить слово", command=self.add_word).grid(column=0, row=1,
                                                                                        sticky=W + E, padx=5, pady=5)
        self.root.bind("<Delete>", self.allbind)
        self.root.bind("<Return>", self.allbind)
        self.start_button = Button(text="Начать запись", command=self.kolichestvo).grid(column=0, row=4,
                                                                                        sticky='nsew', padx=5, pady=5)
        sb = Scrollbar(st.root, orient=VERTICAL)
        sb.grid(row=3, column=2, sticky='ns' + E)
        self.languages_listbox = Listbox(width=50, yscrollcommand=sb.set)
        self.languages_listbox.grid(row=3, column=0, columnspan=2, sticky=W + E, padx=5, pady=5)
        sb.config(command=self.languages_listbox.yview)

        mainloop()


st = auio_start()
st.menu()














