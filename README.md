# Naver Cafe Scraper

## Setting up `venv`

---

### 1. Python Version

- You must have python version greater than 3.3

### 2. Activate `venv`

For Mac or Linux

```bash
source ./selenium-venv/bin/activate
```

### For Windows

```bash
./activate/Scripts/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## How to use

---

### 1. Setup `.env` environment file

- Make a new file with name `.env` in the root directory
- Following is the example of `.env` file

```bash
# .env
CAFE_URL=https://cafe.example.com
USERID=your_id
PASSWORD=your_password
AUTHOR=author_name
```

### 2. Run `main.py` file

```bash
python main.py
```

### 3. Check the result

- You can see the result in screenshots in `result` directory
