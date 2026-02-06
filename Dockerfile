# ============================================
# STAGE 1: Builder - instalacja zależności
# ============================================
FROM python:3.11-slim as builder

WORKDIR /app

# Kopiuje tylko requirements żeby wykorzystać cache
COPY requirements.txt .

# Instaluje zależności do osobnego folderu
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ============================================
# STAGE 2: Runtime - lekki obraz produkcyjny
# ============================================
FROM python:3.11-slim as runtime

WORKDIR /app

# Kopiuje zainstalowane paczki z buildera
COPY --from=builder /install /usr/local

# Kopiuje kod aplikacji
COPY app/ ./app/

# Port na którym działa aplikacja
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Uruchomienie aplikacji
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
