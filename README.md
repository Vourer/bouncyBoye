# bouncyBoye
Projekt na PA - Symulowanie odbijającej się piłki

Opis plików:
- program.py - plik odpowiedzialny za symulację piłki, tworzenie wykresów itp. 
- app.py - plik obsługujący Flask
- baza.html - template pod strony z rozszerzeniami html
- index.html - strona główna, zawierająca formularz; rozwinięcie baza.html
- wynik.html - strona na którą przekierowuje przycisk 'Przeprowadź symulację', zawierająca dane i wykresy powstałe w symulacji
- styl.css - arkusz stylów obsługujący formatowanie wyglądu strony

Prawidłowy układ plików powinien wyglądać następująco:
bouncyBoye/
  templates/
     baza.html
     index.html
     wynik.html
  static/
     styl.css
  app.py
  program.py
