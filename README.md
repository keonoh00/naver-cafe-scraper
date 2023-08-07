# Naver Cafe Scraper

This repository is to scrape the Naver Cafe.

## Setup Project

This repository is built on Python 3.8.5

### 1. Create `venv`

You can create `venv` by following command

```bash
python -m venv venv
```

### 2. Activate `venv`

#### For Mac or Linux

```bash
source ./venv/bin/activate
```

#### For Windows

```bash
./venv/Scripts/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## How to use

### 1. Setup `.env` environment file

- Make a new file with name `.env` in the root directory
- Following is the example of `.env` file

```bash
# .env
CAFE_URL=https://cafe.example.com
USERID=your_id
PASSWORD=your_password
AUTHOR=author_name
SAVE_DIR=<path to your result>
```

### 2. Run `main.py` file

```bash
python main.py
```

### 3. Check the result

- You can see the result in screenshots in `<path to your result>` directory
