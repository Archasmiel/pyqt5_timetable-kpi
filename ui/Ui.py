import requests as req
import re

from PyQt5 import QtWidgets, uic, QtGui

UIfile = 'ui/app.ui'


def create_table_start(table_id):
    return f'<table id="ctl00_MainContent_{table_id}ScheduleTable" class="table table-bordered table-hover" ' \
           f'cellpadding="10" rules="all" align="center" border="1">'


def custom_table_start(table_id):
    return f'<table id="ctl00_MainContent_{table_id}ScheduleTable" class="table table-bordered table-hover" ' \
           f'cellpadding="10" cellspacing="0" rules="all" align="center" border="1" bordercolor="gray">'


def remove_links(html_text, colors):
    text = ''
    ignore, ignored = read_ignore()

    re1, re2 = '<a[^\>]+">', '</a>'
    color1, color2 = colors[0], colors[1]
    days = '<td></td><td>Понеділок</td><td>Вівторок</td>' \
           '<td>Середа</td><td>Четвер</td><td>П\'ятниця</td><td>Субота</td>'

    for i in html_text.split('\n'):

        if days in i:
            i = re.sub(days, f'<td style="color:#000000" bgcolor={color1}></td>'
                             f'<td style="color:#000000" bgcolor={color1}>Понеділок</td>'
                             f'<td style="color:#000000" bgcolor={color1}>Вівторок</td>'
                             f'<td style="color:#000000" bgcolor={color1}>Середа</td>'
                             f'<td style="color:#000000" bgcolor={color1}>Четвер</td>'
                             f'<td style="color:#000000" bgcolor={color1}>П\'ятниця</td>'
                             f'<td style="color:#000000" bgcolor={color1}>Субота</td>', i)

        search = re.search('[0-9]<br>[0-9]+:[0-9]+', i)
        if search:
            i = re.sub(f'<td>{search.group()}</td>', f'<td style="color:#000000" bgcolor={color1}>{search.group()}</td>', i)

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

        if ignore:
            for j in ignored:
                if len(j) == 1:

                    ind = f'<span class="disLabel">{j[0]}<\/span><br\/>[^\>]+<br\/>[^\>]+ <font color={color2}><br>[^\>]+<\/font>'
                    if j[0] in i:
                        i = re.sub(ind, '', i)

        if 'class="day_backlight"' in i:
            i = re.sub('class="day_backlight"', 'style="color:#000000" bgcolor=#ace2de', i)
        if 'class="current_pair"' in i:
            i = re.sub('class="current_pair"', 'style="color:#000000" bgcolor=#b0d751', i)
        if 'class="closest_pair"' in i:
            i = re.sub('class="closest_pair"', 'style="color:#000000" bgcolor=#ebcf81', i)

        text += i + '\n'

    return text


def process_table(text, index):
    orig_starts = [create_table_start("First"), create_table_start("Second")]
    cust_starts = [custom_table_start("First"), custom_table_start("Second")]
    res = ''
    table_start, table_end, table_bool = orig_starts[index], '</table>', False

    for i in text.split('\n'):
        if table_bool:
            res += f'{i}\n'

        if (table_start in i) and (not table_bool):
            table_bool = True
            res += f'{cust_starts[index]}\n'

        if (table_end in i) and table_bool:
            table_bool = False
            res += f'{table_end}\n'
            break

    return res


def get_group(link: str, group: str):
    resp = req.get(rf'{link}/{group}').text.split('\n')
    for i in resp:
        if 'group_url' in i:
            return i[22:-1]
    return 'no_group'


def read_ignore():
    with open(r'data/ignore.txt', 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
        ignore = True if data[0] == "yes" else False
        content = []
        if len(data) > 1:
            for i in data:
                if not (i == 'yes' or i == 'no'):
                    content.append(i.split('<br>'))

    return ignore, content


def get_dark_theme():
    white = QtGui.QColor(255, 255, 255)
    red = QtGui.QColor(255, 0, 0)
    grey = QtGui.QColor(40, 40, 40)
    black = QtGui.QColor(0, 0, 0)
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, grey)
    palette.setColor(QtGui.QPalette.WindowText, white)
    palette.setColor(QtGui.QPalette.Base, grey)
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, white)
    palette.setColor(QtGui.QPalette.ToolTipText, white)
    palette.setColor(QtGui.QPalette.Text, white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, black)
    palette.setColor(QtGui.QPalette.BrightText, red)
    palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.HighlightedText, black)
    return palette


def get_light_theme():
    white = QtGui.QColor(255, 255, 255)
    red = QtGui.QColor(255, 0, 0)
    black = QtGui.QColor(0, 0, 0)
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, white)
    palette.setColor(QtGui.QPalette.WindowText, black)
    palette.setColor(QtGui.QPalette.Base, white)
    palette.setColor(QtGui.QPalette.AlternateBase,QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, white)
    palette.setColor(QtGui.QPalette.ToolTipText, white)
    palette.setColor(QtGui.QPalette.Text, black)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, black)
    palette.setColor(QtGui.QPalette.BrightText, red)
    palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.HighlightedText, black)
    return palette


def load_colors():
    with open(r'data/colors.txt', 'r') as f:
        data = f.read().split('\n')
    return data[0], data[1], 1 if data[2] == 'dark' else 0


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(UIfile, self)

        self.color1, self.color2, self.theme = load_colors()

        self.tables = [self.textBrowser, self.textBrowser_2]

        self.themes = (
            (get_light_theme, QtGui.QColor(0, 0, 0)),
            (get_dark_theme, QtGui.QColor(255, 255, 255))
        )

        self.setWindowTitle('КПИ расписание')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.set_theme()
        self.pushButton.clicked.connect(self.search_group)
        self.pushButton_2.clicked.connect(self.change_theme)
        self.show()

    def show_table(self, html_text, i):
        self.tables[i].setText(process_table(html_text, i))
        self.tables[i].show()
        self.tables[i].raise_()

    def set_theme(self):
        self.setPalette(self.themes[self.theme][0]())
        self.textBrowser.setPalette(self.themes[self.theme][0]())
        self.textBrowser_2.setPalette(self.themes[self.theme][0]())
        self.lineEdit.setPalette(self.themes[self.theme][0]())
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, self.themes[self.theme][1])
        self.statusBar.setPalette(palette)
        self.pushButton_2.setText('L' if self.theme == 0 else 'D')

    def change_theme(self):
        # 0 - light, 1 - dark
        self.theme = 1 if self.theme == 0 else 0
        self.set_theme()

    def search_group(self):
        if self.sender().text() == self.pushButton.text():
            group_link = get_group('http://api.rozklad.org.ua/v2/groups',
                                   self.lineEdit.text() if self.lineEdit.text() else 'f')

            if group_link == 'no_group':
                self.statusBar.showMessage('Такой группы не найдено.')
                return
            self.statusBar.showMessage(f'Найдено {self.lineEdit.text()}: {group_link}.')

            html_text = remove_links(req.get(group_link).text, (self.color1, self.color2))
            self.show_table(html_text, 0)
            self.show_table(html_text, 1)