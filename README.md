# RED ACCESS — beginner SQL Injection CTF

A tiny, intentionally vulnerable Flask app. The login form is
vulnerable to SQL Injection; the goal is to use that to log in as
`admin` and read `flag.txt` on the admin page. Normal users (e.g. the
seeded `guest` account) cannot reach `/admin` or the flag.

This is for **local, offline practice only**. Do not deploy it on a
public network.

## Setup

```bash
cd red-access
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

The app initializes `red_access.db` automatically on first run.
Visit **http://127.0.0.1:5000**.

## Challenge

- A `guest / guest123` account is provided so you can see a normal,
  non-admin session.
- The real goal is to authenticate as `admin` **without** knowing the
  admin password, by exploiting the login query.
- Reaching `/admin` as admin reveals the contents of `flag.txt`.
- Visiting `/admin` as `guest`, or without logging in, returns `403`.

Give the login form a username that breaks out of the SQL string
rather than just being a string the query compares — that's the whole
challenge. No further hints are provided in the app itself.

## Resetting

Delete `red_access.db` and restart `python3 app.py` to reseed the
database.

## Project layout

```
red-access/
├── app.py            # routes, the vulnerable login query, admin guard
├── init_db.py         # creates & seeds the SQLite database
├── flag.txt           # only ever read inside the /admin role check
├── requirements.txt
├── static/style.css
└── templates/
    ├── login.html
    ├── dashboard.html
    ├── admin.html
    └── denied.html
```
