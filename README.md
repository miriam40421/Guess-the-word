
# 🎮 Guess the Word – Python Game

## 📘 Overview  
This is a command-line word guessing game written in Python. The user tries to guess a hidden word letter by letter. The game includes user management, persistent statistics, and unique user identification.

---

## ✨ Features

- 🔤 Guess words one letter at a time
- 🧠 Random word selection from a predefined list
- 👤 User management with name, ID, and password
- 💾 Store statistics per user: number of games, wins, guessed words
- 📊 View game statistics after each session
- 🔁 Option to restart or exit after each round

---

## 🛠 Technologies Used

- Python 3.7+
- Modules:
  - `random`
  - `json`
  - `uuid`
  - `os`

---

## 🗂 File Structure

```
guess_word_game/
├── game.py
├── hugman.py
├── server.py
├── client.py
├── users.txt           # User data stored in JSON format
└── README.md
```

---

## 📄 User Data Format (`users.txt`)

```json
{
  "name": "Sara",
  "id": "c0e8d93b-a234-4bd7-9982-1234567890ab",
  "password": "1234",
  "count": 5,
  "wins": 3,
  "words": ["apple", "train", "music"]
}
```

---

## ▶️ How to Run

1. Open a terminal in the project directory
2. Run the main game file:
   ```bash
   python game.py
   ```
3. (If applicable – for server/client version):
   ```bash
   python server.py
   python client.py
   ```

---

## 📄 License

MIT

---

## 📬 Contact

For support or questions: miriam40421@gmail.com
