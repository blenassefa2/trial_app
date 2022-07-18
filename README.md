# Final Project: *“Mad-words”*
Hello, world!
## Table of contents
* About the website
* Description
* How to use
* Requirements

## About the website

This is my final project for [Harvard CS50x](https://cs50.harvard.edu/x/2020/) course. Since our world is in a pandemic and almost every country is in lockdown, I created an interactive web application  to ease the boredom of quarantine.Since it is integrated with google translate it functions in most languages. It is named *“Mad-words”* and you can play the famous word game *"Mad-lib"* on it.  It is easy and fun to play alone or with people.

 If logged in, you will be able to access different sections of this website. To play you can choose from available stories of specific themes and popularity or create your own story that you can save as public or private. If you want to find a particular story, you can use the search section. You can also edit/delete your account without affecting your stories (But if you delete your account your private stories (not the public ones) and history will also be deleted).

## Description
*“Mad-words”* is a Web application based on Flask framework. I used [cs50 python lib](https://github.com/cs50/python-cs50) for working with database, it can be freely downloaded from GitHub or replaced with something like SQLite.

## How to use

To run the web application use these commands:

```
$ py -m venv env
$ set FLASK_APP=application.py
$ flask run
```
## Requirements

- Python 3
- Flask
- cs50
- Flask-Session
