## KPI Timetable

<details><summary >
<font size="4"> Руководство по интерфейсу </font>
</summary>
<p>

Как окно отобразится если открыть программу:<br>
<img alt="alt text" src="https://github.com/Archasmiel/timetable_kpi_pyqt5/blob/main/examples/example1.png?raw=true" width="450"/>

- Слева снизу область для введения группы.<br>
- Справа снизу кнопка для вызова поиска расписания.Также можно нажать Enter после ввода группы - результат идентично кнопке.<br>
- Справа от "Найти" - кнопка для смены цветовой темы с тёмной на светлую и со светлой на тёмную.<br>
- В самом низу область статуса где будет отображатся информация об успехе или провале поиска.

<br>

- Вводим группу, нажимаем поиск. В итоге заполнятся две панели.<br> 
   1. Верхняя - расписание первой недели.<br>
   2. Нижняя - расписание второй недели.<br>
   3. Подсветка занятия на текущее время, установленное на компьютере

Пример поиска и успешного результата:<br>
<img alt="alt text" src="https://github.com/Archasmiel/timetable_kpi_pyqt5/blob/main/examples/example2.png?raw=true" width="450"/>


Если группы не найдено или пустая строка в вводе - снизу появится характерная надпись.

</p></details>

<details><summary>
<font size="4"> Руководство по игнорированию выборочных предметов </font>
</summary><p>

Для данного действия необходимо:
   - открыть расписание в первый раз и скопировать !ТОЛЬКО НАЗВАНИЕ! нужного предмета<br><img alt="alt text" src="https://github.com/Archasmiel/timetable_kpi_pyqt5/blob/main/examples/example3.png?raw=true" width="450"/>
   - открыть в папке программы папку data<br><img alt="alt text" src="https://github.com/Archasmiel/timetable_kpi_pyqt5/blob/main/examples/example4.png?raw=true" width="450"/>
   - найти файл ignored.txt, открыть в блокноте и вставить новую строчку с названием предмета<br><img alt="alt text" src="https://github.com/Archasmiel/timetable_kpi_pyqt5/blob/main/examples/example5.png?raw=true" width="450"/>
   - сохранить файл
   - перезапустить программу<br><img alt="alt text" src="https://github.com/Archasmiel/timetable_kpi_pyqt5/blob/main/examples/example6.png?raw=true" width="450"/>

</p></details>

<details><summary>
<font size="4"> Руководство по смене цветов </font>
</summary><p>

- Для данного действия необходимо:
   - открыть в папке программы папку data<br><img alt="alt text" src="https://github.com/Archasmiel/timetable_kpi_pyqt5/blob/main/examples/example4.png?raw=true" width="450"/>
   - найти файл ignored.txt, открыть в блокноте
   - в первых двух строчках возможно менять [HEX-коды HTML](https://ru.wikipedia.org/wiki/HTML-цвета) цветов расписания
   - в третьей строчке возможно задать первоначальную тему (light - светлая, dark-тёмная)
   - убедится что в файле три строчки с данными и нет никаких пробелов и пропусков

</p></details>