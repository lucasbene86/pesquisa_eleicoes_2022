# c_1 = Bolsonaro
# c_2 = Ciro Gomes
# c_3 = João Doria
# c_4 = Lula
# c_5 = Mandeta
# c_6 = Em branco
# c_7 = Não sabe

# Probabilidade para total dos votos dos candidatos #
def porcentagem_votos(c_1, c_2, c_3, c_4, c_5, c_6, c_7):
    c1 = float((c_1 * 100) / (c_1 + c_2 + c_3 + c_4 + c_5 + c_6 + c_7))
    c2 = float((c_2 * 100) / (c_1 + c_2 + c_3 + c_4 + c_5 + c_6 + c_7))
    c3 = float((c_3 * 100) / (c_1 + c_2 + c_3 + c_4 + c_5 + c_6 + c_7))
    c4 = float((c_4 * 100) / (c_1 + c_2 + c_3 + c_4 + c_5 + c_6 + c_7))
    c5 = float((c_5 * 100) / (c_1 + c_2 + c_3 + c_4 + c_5 + c_6 + c_7))
    c6 = float((c_6 * 100) / (c_1 + c_2 + c_3 + c_4 + c_5 + c_6 + c_7))
    c7 = float((c_7 * 100) / (c_1 + c_2 + c_3 + c_4 + c_5 + c_6 + c_7))

    lista_porcentagem = [
        f'{c1:.2f}', f'{c2:.2f}', f'{c3:.2f}',
        f'{c4:.2f}', f'{c5:.2f}', f'{c6:.2f}',
        f'{c7:.2f}']

    return lista_porcentagem