# 🤖 Telegram Bot - ឆាតដូចជាសមាជិកធម្មតា

Bot នេះប្រើ AI (Claude Haiku) ដើម្បីឆ្លើយតបជាមួយសមាជិក group ដូចជាមនុស្សធម្មតា
ដោយមានវិធានក្រុម ការស្វាគមន៍ និង Setting Menu សម្រាប់ម្ចាស់ Bot។

---

## 📋 លក្ខណៈពិសេស

- ✅ ឆ្លើយតបជាភាសាខ្មែរ ធម្មជាតិ ដូចជាមនុស្សធម្មតា
- ✅ ស្វាគមន៍សមាជិកថ្មីដោយស្វ័យប្រវត្តិ
- ✅ `/start` — ណែនាំ Bot
- ✅ `/rules` — បង្ហាញវិធានក្រុម
- ✅ `/setting` — (ម្ចាស់ Bot ប៉ុណ្ណោះ) កំណត់ឈ្មោះ, បុគ្គលិកលក្ខណៈ, វិធាន, សារស្វាគមន៍
- ✅ Toggle ឲ Bot ឆ្លើយគ្រប់សារ ឬតែ Mention/Reply

---

## ⚙️ ការដំឡើង

### ជំហានទី ១ — ទទួល API Keys

**Telegram Bot Token:**
1. ទំនាក់ទំនង [@BotFather](https://t.me/BotFather) នៅ Telegram
2. វាយ `/newbot` → ដាក់ឈ្មោះ → ទទួល Token

**Anthropic API Key:**
1. ចូល [console.anthropic.com](https://console.anthropic.com)
2. Settings → API Keys → Create Key

**Owner ID (Telegram User ID):**
1. ទំនាក់ទំនង [@userinfobot](https://t.me/userinfobot)
2. វាយ `/start` → ទទួល ID

---

### ជំហានទី ២ — ដំឡើង Dependencies

```bash
pip install -r requirements.txt
```

---

### ជំហានទី ៣ — កំណត់ Environment Variables

**វិធីទី ១: .env file (ណែនាំ)**

បង្កើត file ឈ្មោះ `.env` ហើយដាក់:
```
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
ANTHROPIC_API_KEY=sk-ant-api03-...
OWNER_ID=123456789
```

**វិធីទី ២: ផ្លាស់ប្តូរ bot.py ផ្ទាល់**

បើក `bot.py` → ស្វែងរក Config Section → ដាក់ Values:
```python
BOT_TOKEN     = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"
ANTHROPIC_KEY = "sk-ant-api03-..."
OWNER_ID      = 123456789
```

---

### ជំហានទី ៤ — ដំណើរការ Bot

```bash
python bot.py
```

---

## 🎮 របៀបប្រើ

### សម្រាប់សមាជិកធម្មតា

| ពាក្យបញ្ជា | មុខងារ |
|---|---|
| `/start` | ស្វាគមន៍ + ណែនាំ |
| `/rules` | មើលវិធានក្រុម |
| @mention Bot | ឆ្លើយតប |
| Reply ទៅ Bot | ឆ្លើយតប |

### សម្រាប់ម្ចាស់ Bot (Owner)

| ពាក្យបញ្ជា | មុខងារ |
|---|---|
| `/setting` | បើក Menu ការកំណត់ |

**Menu /setting រួមមាន:**
- 📝 ផ្លាស់ប្តូរឈ្មោះ Bot
- 🎭 ផ្លាស់ប្តូរបុគ្គលិកលក្ខណៈ (Personality)
- 📋 ផ្លាស់ប្តូរវិធានក្រុម
- 👋 ផ្លាស់ប្តូរសារស្វាគមន៍
- 💬 Toggle ការឆ្លើយ Group (ឆ្លើយគ្រប់សារ / ឆ្លើយតែ Mention)
- 📊 មើលស្ថានភាព Bot
- 🔄 Reset ការកំណត់ Default

---

## 📁 Structure

```
telegram_bot/
├── bot.py            ← Code ចម្បង
├── requirements.txt  ← Dependencies
├── settings.json     ← ការកំណត់ (បង្កើតដោយស្វ័យប្រវត្តិ)
└── README.md         ← ឯកសារនេះ
```

---

## ☁️ ដំណើរការ 24/7 (ជម្រើស)

**ដោយប្រើ screen (Linux/VPS):**
```bash
screen -S mybot
python bot.py
# Ctrl+A+D ដើម្បីចេញ
```

**ដោយប្រើ systemd service:**
```ini
[Unit]
Description=Telegram Bot

[Service]
ExecStart=/usr/bin/python3 /path/to/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## ❓ ចម្ងល់ / បញ្ហា

- Bot មិនឆ្លើយ → ពិនិត្យ BOT_TOKEN ត្រឹមត្រូវ
- `/setting` មិនដំណើរការ → ពិនិត្យ OWNER_ID ត្រឹមត្រូវ
- ឆ្លើយជាភាសាអង់គ្លេស → ពិនិត្យ Personality ក្នុង `/setting`
