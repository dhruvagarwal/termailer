Termailer
=========

**Description**  
A Python script to send email from terminal directly.  

Email-providers supported:

- Gmail
- Yahoo
- Outlook
- Hotmail
- Yandex
- AOL
- Zoho
- iCloud

    *NOTE*: If you use any other domain, you can just add it to the settings.py file.

**How to Use ?**
Locate yourself in parent directory of this project.(Or add it in your path)

    python -m termailer.termailer

**FAQ**
 - *Why am I getting a 534 error code with Gmail?*
 This is so because Gmail prevents authorization by so called "less secure apps" by default.
 To change this, sign-in to your Gmail account, go to [this link][1] and select **Turn on**.

[1]:https://www.google.com/settings/security/lesssecureapps
