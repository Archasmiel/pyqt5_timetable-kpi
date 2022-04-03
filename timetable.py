import requests as req
import sys
import re

from PyQt5 import QtWidgets, uic, QtGui

UIfile = 'ui/app.ui'


def create_table_start(table_id):
    return f'<table id="ctl00_MainContent_{table_id}ScheduleTable" class="table table-bordered table-hover" ' \
           f'cellpadding="10" rules="all" align="center" border="1">'


def remove_links(html_text):
    text = ''

    re1, re2 = '<a[^\>]+">', '</a>'
    for i in html_text.split('\n'):
        color1, color2 = '#5B7DB1', '#61A4BC'

        days = '<td></td><td>Понеділок</td><td>Вівторок</td>' \
               '<td>Середа</td><td>Четвер</td><td>П\'ятниця</td><td>Субота</td>'

        if days in i:
            i = re.sub(days, f'<td></td>'
                             f'<td><font color={color1}>Понеділок</font></td>'
                             f'<td><font color={color1}>Вівторок</font></td>'
                             f'<td><font color={color1}>Середа</font></td>'
                             f'<td><font color={color1}>Четвер</font></td>'
                             f'<td><font color={color1}>П\'ятниця</font></td>'
                             f'<td><font color={color1}>Субота</font></td>', i)

        search = re.search('[0-9]<br>[0-9]+:[0-9]+', i)
        if search:
            i = re.sub(search.group(), f'<font color={color1}>{search.group()}</font>', i)

        search = re.search('Лек on-line', i)
        if search:
            i = re.sub(search.group(), f'<font color={color2}>{"<br>Лекція online"}</font>', i)

        search = re.search('Прак on-line', i)
        if search:
            i = re.sub(search.group(), f'<font color={color2}>{"<br>Практика online"}</font>', i)

        search = re.search('Лаб on-line', i)
        if search:
            i = re.sub(search.group(), f'<font color={color2}>{"<br>Лабораторна online"}</font>', i)

        if '<a class="plainLink" href=' in i:
            i = re.sub(re1, '', i)
            i = re.sub(re2, '', i)

        text += i + '\n'

    return text


def process_table(text, i):
    res = ''
    table_start, table_end, table_bool = table_starts[i], '</table>', False

    for i in text.split('\n'):
        if table_bool:
            res += f'{i}\n'

        if (table_start in i) and (not table_bool):
            table_bool = True
            res += f'{i}\n'

        if (table_end in i) and table_bool:
            table_bool = False
            break
    return res


def get_group(link: str, group: str):
    resp = req.get(rf'{link}/{group}').text.split('\n')
    for i in resp:
        if 'group_url' in i:
            return i[22:-1]
    return 'no_group'


table_starts = [create_table_start("First"), create_table_start("Second") ]


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(UIfile, self)
        self.tables = [self.textBrowser, self.textBrowser_2]
        self.pushButton.clicked.connect(self.button_clicked)
        self.setWindowIcon(QtGui.QIcon('ui/icon.png'))
        self.setWindowTitle('КПИ расписание')
        self.show()

    def show_table(self, html_text, i):
        self.tables[i].setText(process_table(html_text, i))
        self.tables[i].show()
        self.tables[i].raise_()

    def button_clicked(self):

        if self.sender().text() == self.pushButton.text():
            group_link = get_group('http://api.rozklad.org.ua/v2/groups',
                                   self.lineEdit.text() if self.lineEdit.text() else 'press-f')

            if group_link == 'no_group':
                self.statusBar.showMessage('Такой группы не найдено.')
                return
            self.statusBar.showMessage(f'Найдено {self.lineEdit.text()}: {group_link}.')

            html_text = remove_links(req.get(group_link).text)
            self.show_table(html_text, 0)
            self.show_table(html_text, 1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = Ui()
    app.exec_()


if __name__ == "__main__":
    main()
