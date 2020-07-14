# useful_tools
A curated list of useful tools (mini-projects).

**Projects**:
- [password_checker](https://github.com/OAndris/useful_tools/tree/master/password_checker): Check if your passwords have ever been hacked (based on the "https://haveibeenpwned.com/" API).
Passwords are read from "passwords.txt", separated by newline (thus they are not passed to and cannot be saved by the command line).
They are hashed via SHA1 (thus they are converted by a one-way algorithm and not used directly),
and only the first 5 characters of the password hash are sent to the API (thus the full hash remains unknown and the password cannot be reverse engineered with brute force).
- [pdf_processing](https://github.com/OAndris/useful_tools/tree/master/pdf_processing): Process PDF files. For example, add watermarks, rotate specific pages, or merge multiple files.
- [scrape_hackernews](https://github.com/OAndris/useful_tools/tree/master/scrape_hackernews): Collect the articles from multiple Hacker News pages, filter and order them based on the number of votes, and output to a HTML page or to the console.
- [sms_sending_twilio](https://github.com/OAndris/useful_tools/tree/master/sms_sending_twilio): Send custom SMS to any phone number, using Twilio.
- [text_translator](https://github.com/OAndris/useful_tools/tree/master/text_translator): Translate a text from one language to another.
- [url_to_png](https://github.com/OAndris/useful_tools/tree/master/url_to_png) Record and save the entire page from multiple URLs to screenshots. The input 'urls' is a dictionary of custom names and URLs. Requires 'chromedriver.exe'.
