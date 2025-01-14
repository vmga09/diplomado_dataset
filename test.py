import re

def clean_text(text):
    # Eliminar emojis usando expresiones regulares
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticones
        u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
        u"\U0001F680-\U0001F6FF"  # símbolos de transporte & mapas
        u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
        u"\U00002702-\U000027B0"
        u"\U00002700-\U000027BF"  # dingbats
        u"\U0000FE0F"  # VS16
        u"\U0001F900-\U0001F9FF"  # símbolos suplementarios
        "]+", flags=re.UNICODE)
    
    # Eliminar emojis
    text = emoji_pattern.sub('', text)
    
    # Reemplazar múltiples espacios en blanco por uno solo
    text = re.sub(r'\s+', ' ', text)
    
    # Eliminar espacios al inicio y final
    text = text.strip()
    
    return text

# Texto de ejemplo
texto = """🕎 Happy Hanukkah from A2SV! 🕎                                                                                                                                                                                                            

As we light the menorah this season, we celebrate the power of perseverance, the warmth of community, and the light that shines even in the darkest times.
To our students, partners, and supporters—you are the light of our mission, illuminating the path toward innovation, education, and opportunity.
May this Hanukkah bring you joy, peace, and moments of connection with those who matter most. Together, we'll continue to spark hope and transform lives across the globe.
Wishing you a bright and meaningful Hanukkah and an inspiring year ahead! 🌟
#a2sv #HappyHanukkah #A2SVCommunity #FestivalOfLights #Gratitude
🎄 Merry Christmas from A2SV! 🎄"""

# Limpiar el texto
texto_limpio = clean_text(texto)
print(texto_limpio)