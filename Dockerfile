# Python 3.10 tabanlı bir image kullanıyoruz
FROM python:3.10.5

# Çalışma dizinini belirliyoruz
WORKDIR /app

# Gereksinim dosyasını container'a kopyalıyoruz
COPY requirements.txt .

# Gereksinim dosyasındaki bağımlılıkları kuruyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Python dosyasını kopyalıyoruz
COPY . .

# Container çalıştırıldığında bu komutu çalıştıracağız
CMD ["python", "main.py"]
