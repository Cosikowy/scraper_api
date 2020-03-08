# Mikroserwis do pobierania zawartości strony i obiektów `<img>`

Zbudowanie mikroserwisu w dockerze

`docker build -t scraper .`

Uruchomienie mikroserwisu na domyślnym porcie 5000

`docker run -it -p 5000:5000 scraper`

Struktura mikroserwisu

    ├── downloaded                  # Folder ze ściągniętą zawartością
    ├── logic                       # Logika scrapera
    ├── resources                   # Endpointy zasobów
    ├── routes                      # Routing i config aplikacji flaska
    ├── temp                        # Folder zapisanymi archiwami zip do pobrania 
    ├── tests                       # Testy automatyczne
    ├── Dockerfile
    ├── LICENSE
    ├── README.md
    ├── run.py
    └── requirements.txt