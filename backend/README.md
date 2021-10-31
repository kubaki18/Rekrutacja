#Dokumentacja

Aplikacja napisana w Pythonie za pomocą frameworka Django.
Opiera się na bazie danych SQLite.
Główna część aplikacja znajduje się w ./backend/django/myapi/app/views.py
Zaimplementowane modele danych różnią się nieco od tych podanych w specyfikacji. Przede wszystkim, rezerwacje nie uwzględniają daty i czasu trwania rezerwacji, a dwie daty (początek i koniec).
Dodałem do projektu importowalny config do Postmana, w którym przygotowane są zapytania w odpowiedniej formie dla
zaimplementowanych modeli.
