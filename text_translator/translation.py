"""
Idea based on "Complete Python Developer in 2020: Zero to Mastery" from Andrei Neagoie.
"""

from translate import Translator  # https://pypi.org/project/translate/


filename = "short.txt"
to_lang = 'de'
translator = Translator(to_lang=to_lang, from_lang='en', provider='mymemory')
limit = 500
try:
    with open(filename, mode='r') as source_file:
        with open(f'{to_lang}_{filename}', mode='w') as output_file:
            source_content = source_file.read()
            if len(source_content) <= limit:
                output_file.write(translator.translate(source_content))
            else:
                phrases = source_content.split('. ')
                for phrase in phrases:
                    translated_phrase = translator.translate(phrase)
                    output_file.write(f"{translated_phrase}. ")
                    print("=========")
                    print(phrase)
                    print()
                    print(translated_phrase)
                    print()
except FileNotFoundError as err:
    print("Please provide a file.")
