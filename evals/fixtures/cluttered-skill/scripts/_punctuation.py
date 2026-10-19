def normalize(text):
    return text.translate(str.maketrans({"，": ",", "。": "."}))
