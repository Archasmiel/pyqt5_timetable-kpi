import requests as req
import sys

from PyQt5 import QtWidgets, uic

UIfile = 'ui/app.ui'

table_starts = [
    '<table id="ctl00_MainContent_FirstScheduleTable" class="table table-bordered table-hover" cellpadding="10" '
    'rules="all" align="center" border="1">',
    '<table id="ctl00_MainContent_SecondScheduleTable" class="table table-bordered table-hover" cellpadding="10" '
    'rules="all" align="center" border="1">',
]
table_ends = [
    '</table>',
    '</table>',
]
table_bools = [
    False,
    False,
]


def process_table(html_text, num):
    table = ''
    table_bool = table_bools[num - 1]
    table_start = table_starts[num - 1]
    table_end = table_ends[num - 1]
    for i in html_text.split('\n'):
        if table_bool:
            table += f'{i}\n'

        if (table_start in i) and (not table_bool):
            table_bool = True
            table += f'{i}\n'

        if (table_end in i) and table_bool:
            table_bool = False
            break
    return table


def get_group(link: str, group: str):
    resp = req.get(rf'{link}/{group}').text.split('\n')
    for i in resp:
        if 'group_url' in i:
            return i[22:-1]
    return 'no_group'


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(UIfile, self)
        self.pushButton.clicked.connect(self.button_clicked)
        self.show()

    def button_clicked(self):

        sender = self.sender()
        if sender.text() == 'Найти расписание':
            group_name = self.lineEdit.text()
            print(self.lineEdit.text())
            if len(group_name) > 0:
                group_link = get_group('http://api.rozklad.org.ua/v2/groups', group_name)
                if group_link == 'no_group':
                    self.statusBar.showMessage('Такой группы не найдено.')
                    return
                self.statusBar.showMessage(f'{group_name}: {group_link}')
            else:
                self.statusBar.showMessage('Такой группы не найдено.')
                return

            html_text = req.get(group_link).text

            table1 = process_table(html_text, 1)
            self.textBrowser.setText(table1)
            self.textBrowser.show()
            self.textBrowser.raise_()

            table2 = process_table(html_text, 2)
            self.textBrowser_2.setText(table2)
            self.textBrowser_2.show()
            self.textBrowser_2.raise_()


app = QtWidgets.QApplication(sys.argv)
window = Ui()

app.exec_()
