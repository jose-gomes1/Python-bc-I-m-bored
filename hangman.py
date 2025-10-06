import random

palavras = {
    "Frutas": [
        "Banana", "Maca", "Pera", "Laranja", "Abacaxi",
        "Manga", "Morango", "Melancia", "Kiwi", "Uva",
        "Cereja", "Ameixa", "Limao", "Figo", "Maracuja",
        "Abacate", "Framboesa", "Coco", "Tangerina", "Goiaba"
    ],
    "Animais": [
        "Gato", "Cao", "Elefante", "Leao", "Tigre",
        "Girafa", "Cavalo", "Coelho", "Macaco", "Rato",
        "Urso", "Lobo", "Tartaruga", "Golfinho", "Peixe",
        "Canguru", "Zebra", "Cobra", "Pinguim", "Coruja"
    ],
    "Cores": [
        "Vermelho", "Azul", "Verde", "Amarelo", "Preto",
        "Branco", "Rosa", "Roxo", "Laranja", "Cinzento",
        "Marrom", "Bege", "Turquesa", "Lilas", "Dourado",
        "Prata", "Magenta", "Ciano", "Violeta", "Salmao"
    ],
    "Paises": [
        "Brasil", "Portugal", "Espanha", "Franca", "Alemanha",
        "Italia", "Japao", "China", "Canada", "Estados Unidos",
        "Argentina", "Mexico", "Russia", "Australia", "india",
        "Egito", "Grecia", "Noruega", "Suecia", "Chile"
    ],
    "Profissões": [
        "Medico", "Professor", "Engenheiro", "Advogado", "Enfermeiro",
        "Arquiteto", "Motorista", "Padeiro", "Cantor", "Ator",
        "Jornalista", "Cientista", "Piloto", "Chef", "Designer",
        "Dentista", "Veterinario", "Programador", "Fotografo", "Eletricista"
    ],
    "Objetos": [
        "Mesa", "Cadeira", "Caneta", "Livro", "Computador",
        "Telemovel", "Relogio", "oculos", "Bicicleta", "Copo",
        "Chave", "Câmera", "Televisao", "Geladeira", "Fogao",
        "Sofa", "Escova", "Fone", "Livro", "Teclado"
    ]
}


def hangman(dict):
    tema = random.choice(list(dict.keys()))
    palavra = random.choice(dict[tema]).lower()
    letras_descobertas = ["_" for _ in palavra]
    print(f"Tema: {tema}")
    while "_" in letras_descobertas:
        print("Palavra: ", " ".join(letras_descobertas))
        tentativa = input("Tenta uma letra ou a palavra inteira: ").lower()
        if tentativa == palavra:
            letras_descobertas = list(palavra)
            break
        elif len(tentativa) == 1:
            if tentativa in palavra:
                for i, l in enumerate(palavra):
                    if l == tentativa:
                        letras_descobertas[i] = tentativa
            else:
                print("Letra incorreta!")
        else:
            print("Palavra incorreta!")
    print(f"Ganhaste! A palavra era '{palavra}'.")


hangman(palavras)