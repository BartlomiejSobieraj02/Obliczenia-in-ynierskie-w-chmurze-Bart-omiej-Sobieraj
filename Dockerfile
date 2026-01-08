# Obraz bazowy - lekki Linux z Pythonem
FROM python:3.9-slim

# Ustawiamy katalog roboczy
WORKDIR /app

# Instalujemy bibliotekę do obliczeń (jedyna zależność)
RUN pip install numpy

# Kopiujemy nasz kod do kontenera
COPY main.py .

# Domyślna komenda startowa
CMD ["python", "main.py"]