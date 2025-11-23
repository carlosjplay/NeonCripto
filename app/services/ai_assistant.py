FAQS = {
    "o que é market cap": "Market cap é o valor total de mercado: preço x quantidade em circulação.",
    "o que é rsi": "RSI é um oscilador que mede velocidade e mudança dos preços, comum em 14 períodos.",
    "como montar carteira": "Defina objetivos, diversifique por risco/liquidez, rebalanceie e controle a exposição."
}

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    for key, val in FAQS.items():
        if key in q:
            return val
    return "Posso ajudar com conceitos, leitura de indicadores e interpretação dos gráficos. Pergunte algo específico."
