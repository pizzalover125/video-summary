from translate import Translator

def translate_text(text, source_lang, target_lang):
    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    sentences = text.split(".")
    translations = []
    for sentence in sentences:
        translation = translator.translate(sentence)
        translations.append(translation)
    return '. '.join(translations)

# Example usage
text_to_translate = "Hello, how are you? I hope you're doing well. This is a test."
source_language = "en"
target_language = "fr"

translated_text = translate_text(text_to_translate, source_language, target_language)
print(f"Translated text: {translated_text}")