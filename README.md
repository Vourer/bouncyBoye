# bouncyBoye
Projekt na PA - Symulowanie odbijającej się piłki

Opis plików:
- program.py - plik odpowiedzialny za przeprowadzenie symulacji ruchu piłki, tworzenie wykresów itp. 
- app.py - plik obsługujący Flask
- baza.html - template, z kórego korzystają inne pliki z rozszerzeniami html znajdujące się w tym repo
- index.html - strona główna, zawierająca formularz pobierający dane nt. piłki niezbędne do stworzenia symulacji
- wynik.html - strona wynikowa, na którą przekierowuje przycisk 'Przeprowadź symulację'; zawiera dane i wykresy powstałe w symulacji
- styl.css - arkusz stylów odpowiedzialny za wygląd obu stron

Prawidłowy układ plików po pobraniu powinien wyglądać następująco
```
bouncyBoye/
	templates/
		baza.html
		index.html
		wynik.html
	static/
		styl.css
	app.py
	program.py
```
