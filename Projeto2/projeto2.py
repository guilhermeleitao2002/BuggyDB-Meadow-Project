#99951 Guilherme Leitão


'''Este script contém as funções desenvolvidas com o intuito de simular o ecossistema de um prado no qual convivem animais
   que se movimentam, reproduzem, alimentam e morrem. Este prado encontra-se rodeado por montanhas e, no meio do espaço habitável,
   existem os ocasionais rochedos, que são gerados de forma arbitrária.
   
   Existem dois tipos de animais: as presas - herbívoras e que
   por isso não necessitam de se alimentar especificamente, pois o fazem automaticamente do chão do prado - e os predadores -
   carnivoras, ou seja, alimentam-se das presas. A simulação é feita tendo em conta a noção de geração, durante a qual um animal
   está confinado a determinadas ações bem definidas.'''


# TAD posicao > -----------------------------------------------------------------------------------------------------------------------------------------------------


def cria_posicao(x, y):
    # int x int -> posicao
    '''Recebe os inteiros correspondentes às coordenadas de uma posição e devolve a respetiva posição.'''
    if type(x) != int or type(y) != int or x < 0 or y < 0:
        raise ValueError("cria_posicao: argumentos invalidos")
    return (x, y)


def cria_copia_posicao(pos):
    # posicao -> posicao
    '''Como o nome sugere, recebe uma posição e devolve uma cópia da mesma.'''
    if not eh_posicao(pos):
        raise ValueError("cria_posicao: argumentos invalidos")
    return cria_posicao(obter_pos_x(pos), obter_pos_y(pos))


def obter_pos_x(pos):
    # posicao -> int
    '''Recebe uma posição e devolve a sua abscissa.'''
    return pos[0]


def obter_pos_y(pos):
    # posicao -> int
    '''Recebe uma posição e devolve a sua ordenada.'''
    return pos[1]


def eh_posicao(obj):
    # universal -> booleano
    '''Recebe um qualquer argumento e devolve True se e só se esse argumento for uma posição.'''
    return type(obj) == tuple and len(obj) == 2 and type(obter_pos_x(obj)) == int and\
           type(obter_pos_y(obj)) == int and obter_pos_x(obj) >= 0 and obter_pos_y(obj) >= 0


def posicoes_iguais(p1, p2):
    # posicao x posicao -> booleano
    '''Recebe dois quaisquer argumentos e devolve True se e só se estes forem duas posições iguais.'''
    return eh_posicao(p1) and eh_posicao(p2) and obter_pos_x(p1) == obter_pos_x(p2)\
           and obter_pos_y(p1) == obter_pos_y(p2)


def posicao_para_str(pos):
    # posicao -> str
    '''Recebe uma posição e retorna uma cadeia de carateres a representá-la.'''
    return "({}, {})".format(obter_pos_x(pos), obter_pos_y(pos))


def obter_posicoes_adjacentes(pos):
    # posicao -> tuplo
    '''Recebe uma posição e devolve um tuplo de posições adjacentes a esta.'''
    adj = ()
    if obter_pos_y(pos) > 0: # se a posição fornecida não estiver na primeira linha
        adj += (cria_posicao(obter_pos_x(pos), obter_pos_y(pos) - 1),)
    adj += (cria_posicao(obter_pos_x(pos) + 1, obter_pos_y(pos)),) + (cria_posicao(obter_pos_x(pos), obter_pos_y(pos) + 1),)
    if obter_pos_x(pos) > 0: # se a posição fornecida não estiver na primeira coluna
        adj += (cria_posicao(obter_pos_x(pos) - 1, obter_pos_y(pos)),)
    return adj


def ordenar_posicoes(t):
    # tuplo -> tuplo
    '''Recebe um tuplo de posições e devolve um tuplo das mesmas posições mas ordenadas de acordo com a ordem de leitura do prado.'''
    max_x = 0
    # achar, na prática, a maior abscissa a ter em conta nas posições fornecidas
    for pos in t:
        if obter_pos_x(pos) > max_x:
            max_x = obter_pos_x(pos)
    order = []
    # achar o valor numérico N correspondente a cada posição e ordená-los por ordem crescente
    for pos in t:
        order += [obter_pos_y(pos) * (max_x + 1) + obter_pos_x(pos)]
    order.sort()
    ordered = ()
    # ordenar as posições fornecidas de acordo com o respetivo valor numérico definido anteriormente
    for i in range(len(order)):
        for pos in t:
            if obter_pos_y(pos) * (max_x + 1) + obter_pos_x(pos) == order[i]:
                ordered += (cria_copia_posicao(pos),)
    return ordered


# < TAD posicao -----------------------------------------------------------------------------------------------------------------------------------------------------


# TAD animal > ------------------------------------------------------------------------------------------------------------------------------------------------------


def cria_animal(sp, rep, feed):
    # str x int x int -> animal
    '''Recebe uma cadeia de carateres e dois inteiros, contendo, respetivamente, o nome da espécie, a frequência de reprodução
       e a frequência de alimentação e retorna um animal com idade e fome iguais a zero e com os atributos passados.'''
    if type(sp) != str or type(rep) != int or type(feed) != int or len(sp) == 0 or rep <= 0 or feed < 0:
        raise ValueError("cria_animal: argumentos invalidos")
    return [sp, 0, rep] if feed == 0 else [sp, 0, rep, 0, feed]


def cria_copia_animal(obj):
    # animal -> animal
    '''Recebe um animal e retorna uma cópia exata do mesmo.'''
    if not eh_animal(obj):
        raise ValueError("cria_animal: argumentos invalidos")
    return [obter_especie(obj), obter_idade(obj), obter_freq_reproducao(obj)] if len(obj) == 3 else\
           [obter_especie(obj), obter_idade(obj), obter_freq_reproducao(obj), obter_fome(obj), obter_freq_alimentacao(obj)]


def obter_especie(animal):
    # animal -> str
    '''Recebe um animal e retorna uma cadeia de carateres representando o nome da sua espécie.'''
    return animal[0]


def obter_freq_reproducao(animal):
    # animal -> int
    '''Recebe um animal e retorna um inteiro representando a sua frequência de reprodução.'''
    return animal[2]


def obter_freq_alimentacao(animal):
    # animal -> int
    '''Recebe um animal e retorna um inteiro representando a sua frequência de alimentação.'''
    return animal[4] if eh_predador(animal) else 0


def obter_idade(animal):
    # animal -> int
    '''Recebe um animal e retorna um inteiro representando a sua idade.'''
    return animal[1]


def obter_fome(animal):
    # animal -> int
    '''Recebe um animal e retorna um inteiro representando o seu nivel de fome.'''
    return animal[3] if eh_predador(animal) else 0


def aumenta_idade(animal):
    # animal -> animal
    '''Recebe um animal e modifica-o aumentando em uma unidade a sua idade e retorna o mesmo animal alterado.'''
    animal[1] += 1
    return animal


def reset_idade(animal):
    # animal -> animal
    '''Recebe um animal e modifica-o restabelecendo a sua idade igual a zero e retorna o mesmo animal alterado.'''
    animal[1] = 0
    return animal


def aumenta_fome(animal):
    # animal -> animal
    '''Recebe um animal e modifica-o aumentando em uma unidade a sua fome e retorna o mesmo animal alterado.'''
    if eh_predador(animal):
        animal[3] += 1
    return animal


def reset_fome(animal):
    # animal -> animal
    '''Recebe um animal e modifica-o restabelecendo a sua fome igual a zero e retorna o mesmo animal alterado.'''
    if eh_predador(animal):
        animal[3] = 0
    return animal


def eh_animal(obj):
    # universal -> booleano
    '''Recebe um qualquer argumento e retorna True se e só se este corresponder a um animal.'''
    return type(obj) == list and (len(obj) == 3 or len(obj) == 5) and type(obj[0]) == str and len(obj[0]) > 0 and\
           type(obj[1]) == int and obj[1] >= 0 and type(obj[2]) == int and obj[2] >= 0 and (len(obj) == 3 or\
           (len(obj) == 5 and type(obj[3]) == int and obj[3] >= 0 and type(obj[4]) == int and obj[4] >= 0))


def eh_predador(obj):
    # universal -> booleano
    '''Recebe um qualquer argumento e retorna True se e só se este corresponder a um animal predador.'''
    return eh_animal(obj) and len(obj) == 5


def eh_presa(obj):
    # universal -> booleano
    '''Recebe um qualquer argumento e retorna True se e só se este corresponder a um animal presa.'''
    return eh_animal(obj) and len(obj) == 3


def animais_iguais(obj1, obj2):
    # animal x animal -> booleano
    '''Recebe dois animais e retorna True se e só se eles forem animais iguais.'''
    return eh_animal(obj1) and eh_animal(obj2) and obter_especie(obj1) == obter_especie(obj2) and obter_idade(obj1) == obter_idade(obj2)\
           and obter_freq_reproducao(obj1) == obter_freq_reproducao(obj2) and (eh_presa(obj1) and eh_presa(obj2) or eh_predador(obj1) and\
           eh_predador(obj2) and obter_fome(obj1) == obter_fome(obj2) and obter_freq_alimentacao(obj1) == obter_freq_alimentacao(obj2))


def animal_para_char(animal):
    # animal -> str
    '''Recebe um animal e retorna o primeiro carácter do nome da espécie em minúsculo, caso se trate de uma presa, ou em maiúculo, um predador.'''
    return obter_especie(animal)[0].lower() if eh_presa(animal) else obter_especie(animal)[0].upper()


def animal_para_str(animal):
    # animal -> str
    '''Recebe um animal e retorna uma cadeia de caracteres com a devida representação das suas instâncias.'''
    return "{} [{}/{};{}/{}]".format(obter_especie(animal), obter_idade(animal), obter_freq_reproducao(animal), obter_fome(animal), obter_freq_alimentacao(animal))\
           if eh_predador(animal) else "{} [{}/{}]".format(obter_especie(animal), obter_idade(animal), obter_freq_reproducao(animal))


def eh_animal_fertil(animal):
    # animal -> boolenao
    '''Recebe um animal e retorna True se e só se o animal atingiu a idade de reprodução.'''
    return obter_freq_reproducao(animal) <= obter_idade(animal)


def eh_animal_faminto(animal):
    # animal -> booleano
    '''Recebe um animal e retorna True se e só se se trata de um predador e o nivel de fome do animal atingiu ou superou a frequência de alimentação.'''
    return eh_predador(animal) and obter_freq_alimentacao(animal) <= obter_fome(animal)


def reproduz_animal(animal):
    # animal -> animal
    '''Recebe um animal e altera a sua idade para zero, retornando um animal da mesma espécie, com os mesmos valores de frequências, mas com a idade e fome,
       no caso de predador, a zeros.'''
    animal = reset_idade(animal)
    return cria_animal(obter_especie(animal), obter_freq_reproducao(animal), obter_freq_alimentacao(animal))


# < TAD animal ------------------------------------------------------------------------------------------------------------------------------------------------------


# TAD prado > ------------------------------------------------------------------------------------------------------------------------------------------------------


def cria_prado(d, r, a, p):
    # posicao x tuplo x tuplo x tuplo -> prado
    '''Recebe uma posição correspondente à montanha do canto inferior direito, proporcionando as dimensões do prado, um tuplo com zero ou mais
       posições de rochedos, um tuplo com um ou mais animais e um outro tuplo com as respetivas posições dos animais anteriores e retorna
       um prado com todos os atributos passados.'''
    if not eh_posicao(d) or obter_pos_x(d) < 2 or obter_pos_y(d) < 2 or type(r) != tuple or type(p) != tuple or len(a) == 0 or len(p) == 0:
        raise ValueError("cria_prado: argumentos invalidos")
    meadow = [[[] for x in range(obter_pos_x(d) - 1)] for y in range(obter_pos_y(d) - 1)] # criar um prado ignorando as montanhas à volta (simplificar)
    if eh_posicao(r): # se houver apenas um rochedo
        if obter_pos_x(r) >= obter_pos_x(d) or obter_pos_x(r) <= 0 or obter_pos_y(r) >= obter_pos_y(d) or obter_pos_y(r) <= 0:
            raise ValueError("cria_prado: argumentos invalidos")
        meadow[obter_pos_y(r) - 1][obter_pos_x(r) - 1] = "@"
    else: # se eventualmente houver vários rochedos
        for pos in r:
            if not eh_posicao(pos) or obter_pos_x(pos) >= obter_pos_x(d) or obter_pos_x(pos) <= 0 or obter_pos_y(pos) >= obter_pos_y(d) or obter_pos_y(pos) <= 0:
                raise ValueError("cria_prado: argumentos invalidos")
            meadow[obter_pos_y(pos) - 1][obter_pos_x(pos) - 1] = "@"
    if eh_animal(a) and eh_posicao(p): # se houver apenas um animal e respetiva posição
        meadow[obter_pos_y(p) - 1][obter_pos_x(p) - 1] = cria_copia_animal(a)
    else: # se eventualmente houver vários animais
        if type(a) != tuple or type(p) != tuple or len(a) != len(p) or eh_animal(a) or eh_posicao(p):
            raise ValueError("cria_prado: argumentos invalidos")
        for i in range(len(a)):
            if not eh_animal(a[i]) or not eh_posicao(p[i]):
                raise ValueError("cria_prado: argumentos invalidos")
            meadow[obter_pos_y(p[i]) - 1][obter_pos_x(p[i]) - 1] = cria_copia_animal(a[i])
    return meadow


def cria_copia_prado(meadow):
    # prado -> prado
    '''Recebe um qualquer argumento e, caso este seja um prado, retorna uma cópia exata do prado passado.'''
    if not eh_prado(meadow):
        raise ValueError("cria_prado: argumentos invalidos")
    cp = [[[] for x in range(obter_tamanho_x(meadow) - 2)] for y in range(obter_tamanho_y(meadow) - 2)]
    for i in range(obter_tamanho_y(meadow) - 2):
        for j in range(obter_tamanho_x(meadow) - 2):
            if eh_animal(meadow[i][j]):
                cp[i][j] = cria_copia_animal(meadow[i][j])
            else:
                cp[i][j] = meadow[i][j]
    return cp


def obter_tamanho_x(meadow):
    # prado -> int
    '''Recebe um prado e retorna o número de colunas (tem em conta as montanhas à volta).'''
    return len(meadow[0]) + 2


def obter_tamanho_y(meadow):
    # prado -> int
    '''Recebe um prado e retorna o número de linhas (tem em conta as montanhas à volta).'''
    return len(meadow) + 2


def obter_numero_predadores(meadow):
    # prado -> int
    '''Recebe um prado e devolve o número de animais predadores existentes nele.'''
    num = 0
    for i in range(obter_tamanho_y(meadow) - 2):
        for j in range(obter_tamanho_x(meadow) - 2):
            if eh_predador(meadow[i][j]):
                num += 1
    return num


def obter_numero_presas(meadow):
    # prado -> int
    '''Recebe um prado e devolve o número de animais presas existentes nele.'''
    num = 0
    for i in range(obter_tamanho_y(meadow) - 2):
        for j in range(obter_tamanho_x(meadow) - 2):
            if eh_presa(meadow[i][j]):
                num += 1
    return num


def obter_posicao_animais(meadow):
    # prado -> tuplo posicoes
    '''Recebe um prado e devolve um tuplo de todas as posições onde se encontram animais nele.'''
    pos = ()
    for i in range(obter_tamanho_y(meadow) - 2):
        for j in range(obter_tamanho_x(meadow) - 2):
            if eh_animal(meadow[i][j]):
                pos += (cria_posicao(j + 1, i + 1),)
    return pos


def obter_animal(meadow, pos):
    # prado x posicao -> animal
    '''Recebe um prado e uma posição e devolve o animal que se encontra nela.'''
    return meadow[obter_pos_y(pos) - 1][obter_pos_x(pos) - 1]


def eliminar_animal(meadow, pos):
    # prado x posicao -> prado
    '''Recebe um prado e uma posição, modifica-o eliminando o animal da respetiva posição e retorna o mesmo prado.'''
    meadow[obter_pos_y(pos) - 1][obter_pos_x(pos) - 1] = []
    return meadow


def mover_animal(meadow, pos1, pos2):
    # prado x posicao x posicao -> prado
    '''Recebe um prado e duas posições, modifica-o movendo o animal da primeira posição para a segunda e retorna o mesmo prado.'''
    meadow[obter_pos_y(pos2) - 1][obter_pos_x(pos2) - 1] = obter_animal(meadow, pos1)
    eliminar_animal(meadow, pos1)
    return meadow


def inserir_animal(meadow, animal, pos):
    # prado x animal x posicao -> prado
    '''Recebe um prado, um animal e uma posição e introduz destrutivamente no prado o animal na posição indicada, retornando o mesmo prado.'''
    meadow[obter_pos_y(pos) - 1][obter_pos_x(pos) - 1] = animal
    return meadow


def eh_prado(obj):
    # universal -> booleano
    '''Recebe um qualquer argumento e retorna True se e só se este for um prado.'''
    if type(obj) != list or len(obj) < 3:
        return False
    for y in range(obter_tamanho_y(obj) - 2):
        if type(obj[y]) != list or len(obj[y]) < 3:
            return False
        for x in range(obter_tamanho_x(obj) - 2):
            if obj[y][x] != [] and obj[y][x] != "@" and not eh_animal(obj[y][x]):
                return False
    return True


def eh_posicao_animal(meadow, pos):
    # prado x posicao -> booleano
    '''Recebe um prado e uma posição e retorna True se e só se nessa posição se encontrar um animal.'''
    if obter_pos_y(pos) == 0 or obter_pos_x(pos) == 0 or obter_pos_y(pos) == obter_tamanho_y(meadow) - 1 or obter_pos_x(pos) == obter_tamanho_x(meadow) - 1:
        return False
    return eh_animal(meadow[obter_pos_y(pos) - 1][obter_pos_x(pos) - 1])


def eh_posicao_obstaculo(meadow, pos):
    # prado x posicao -> booleano
    '''Recebe um prado e uma posição e retorna True se e só se nessa posição se encontrar um rochedo ou montanha.'''
    return obter_pos_y(pos) == 0 or obter_pos_x(pos) == 0 or obter_pos_y(pos) == obter_tamanho_y(meadow) - 1\
           or obter_pos_x(pos) == obter_tamanho_x(meadow) - 1 or meadow[obter_pos_y(pos) - 1][obter_pos_x(pos) - 1] == "@"


def eh_posicao_livre(meadow, pos):
    # prado x posicao -> booleano
    '''Recebe um prado e uma posição e retorna True se e só se essa posição se encontrar livre.'''
    if obter_pos_y(pos) == 0 or obter_pos_x(pos) == 0 or obter_pos_y(pos) == obter_tamanho_y(meadow) - 1 or obter_pos_x(pos) == obter_tamanho_x(meadow) - 1:
        return False
    return meadow[obter_pos_y(pos) - 1][obter_pos_x(pos) - 1] == []


def prados_iguais(meadow1, meadow2):
    # prado x prado -> booleano
    '''Recebe dois quaisquer argumentos e retorna True se e só se ambos forem prados e tiverem exatamente os mesmos atributos.'''
    if not eh_prado(meadow1) or not eh_prado(meadow2) or len(meadow1) != len(meadow2):
        return False
    for y in range(len(meadow1)):
        for x in range(len(meadow1[0])):
            if meadow1[y][x] != meadow2[y][x] and not animais_iguais(meadow1[y][x], meadow2[y][x]):
                return False
    return True


def prado_para_str(meadow):
    # prado -> str
    '''Recebe um prado e retorna uma cadeia de caracteres com a respetiva representação espacial do mesmo.'''
    # desenhar a primeira linha
    m = "+"
    for i in range(obter_tamanho_x(meadow) - 2):
        m += "-"
    m += "+\n"
    # desenhar as linhas intermédias tendo em conta o que representam
    for i in range(obter_tamanho_y(meadow) - 2):
        m += "|"
        for e in meadow[i]:
            if eh_animal(e): # é uma animal
                m += animal_para_char(e)
            elif e == "@": # é um rochedo
                m += e
            else: # é espaço livre
                m += "."
        m += "|\n"
    # desenhar a última linha
    m += "+"
    for i in range(obter_tamanho_x(meadow) - 2):
        m += "-"
    m += "+"
    return m


def obter_valor_numerico(meadow, pos):
    # prado x posicao -> int
    '''Recebe um prado e uma posição e devolve o valor numérico da posição correspondente nesse prado.'''
    return obter_pos_y(pos) * obter_tamanho_x(meadow) + obter_pos_x(pos)


def obter_movimento(meadow, pos):
    # prado x posicao -> posicao
    '''Recebe um prado e uma posição e devolve a posição que resulta da aplicação das regras de movimento definidas no enunciado.'''
    animal = obter_animal(meadow, pos)
    t_pos2 = obter_posicoes_adjacentes(pos)
    t_pos = ()
    # ignorar as posições com obstáculos, respeitando os casos dos diferentes tipos de animais
    if eh_predador(animal):
        for i in range(len(t_pos2)):
            if not eh_posicao_obstaculo(meadow, t_pos2[i]) and eh_presa(obter_animal(meadow, t_pos2[i])):
                t_pos += (cria_posicao(obter_pos_x(t_pos2[i]), obter_pos_y(t_pos2[i])),)
        if compara_argumentos(len(t_pos), 0):
            for i in range(len(t_pos2)):
                if not eh_posicao_obstaculo(meadow, t_pos2[i]) and eh_posicao_livre(meadow, t_pos2[i]):
                    t_pos += (cria_posicao(obter_pos_x(t_pos2[i]), obter_pos_y(t_pos2[i])),)
    else:
        for i in range(len(t_pos2)):
            if not eh_posicao_obstaculo(meadow, t_pos2[i]) and eh_posicao_livre(meadow, t_pos2[i]):
                t_pos += (cria_posicao(obter_pos_x(t_pos2[i]), obter_pos_y(t_pos2[i])),)
    for i in range(len(t_pos)):
        if compara_argumentos((obter_pos_y(pos) * obter_tamanho_x(meadow) + obter_pos_x(pos)) % len(t_pos), i): # N (mod p)
            return cria_posicao(obter_pos_x(t_pos[i]), obter_pos_y(t_pos[i]))
    return cria_posicao(obter_pos_x(pos), obter_pos_y(pos))


def compara_argumentos(arg1, arg2):
    # universal x universal -> booleano
    '''Função auxiliar que recebe dois quaisquer argumentos e retorna True se e só se estes forem iguais.'''
    return arg1 == arg2


# < TAD prado ------------------------------------------------------------------------------------------------------------------------------------------------------


def geracao(meadow):
    # prado -> prado
    '''Recebe um prado e retorna-o modificado, simulando a passagem de uma geração completa, conforme descrita no enunciado.'''
    animals_p = obter_posicao_animais(meadow) # obter a posição de todos os animais em vez de perder tempo iterando pelo prado inteiro
    black_list = ()
    for i in range(len(animals_p)):
        skip, fed = False, False
        for j in range(len(black_list)):
            if posicoes_iguais(black_list[j], animals_p[i]):
                skip = True
        if skip:
            continue
        animal = obter_animal(meadow, animals_p[i])
        aumenta_idade(animal) # incrementa idade
        aumenta_fome(animal) # incrementa fome
        final_p = obter_movimento(meadow, animals_p[i]) # obter o movimento de eleição para cada animal de acordo com as suas características
        if not posicoes_iguais(final_p, animals_p[i]):
            if eh_predador(animal) and eh_posicao_animal(meadow, final_p) and eh_presa(obter_animal(meadow, final_p)): # ter em conta o caso dos predadores
                fed = True
                black_list += (cria_copia_posicao(final_p),)
            mover_animal(meadow, animals_p[i], final_p)
            if eh_animal_fertil(animal):
                inserir_animal(meadow, reproduz_animal(animal), animals_p[i])
            if fed:
                reset_fome(animal)
            if eh_animal_faminto(animal):
                eliminar_animal(meadow, final_p)
        else:
            if eh_animal_faminto(animal):
                eliminar_animal(meadow, animals_p[i])
    return meadow


def simula_ecossistema(file_name, num, verbose):
    # str x int x booleano -> tuplo
    '''Recebe uma cadeia de caracteres representando o nome do ficheiro onde se encontra a informação sobre o prado e seus constituintes,
       um inteiro número de gerações a simular e um booleano que tem como objetivo ativar a funcionalidade "verbose", permitindo ao utilizador
       receber um feedback mais compreensivo sobre o que se está a passar ao longo das gerações. Finalmente, retorna um tuplo com a
       quantidade final de predadores e presas, respetivamente.'''
    file = open(file_name, "r")
    lines = file.readlines()
    file.close()
    mountain = eval(lines[0])
    rocks_p = eval(lines[1])
    rocks = ()
    for p in rocks_p:
        rocks += (cria_posicao(p[0], p[1]),)
    animals, animals_pos = (), ()
    # gerar um tuplo dos animais do ficheiro e respetivas posições
    for i in range(2, len(lines)):
        animals_i = eval(lines[i])
        animals += (cria_animal(animals_i[0].strip("'"), animals_i[1], animals_i[2]),)
        animals_pos += (cria_posicao(animals_i[3][0], animals_i[3][1]),)
    meadow = cria_prado(cria_posicao(mountain[0], mountain[1]), rocks, animals, animals_pos) # criação do prado de origem
    previous_pred, previous_prey = obter_numero_predadores(meadow), obter_numero_presas(meadow)
    print("Predadores: {} vs Presas: {} (Gen. 0)\n".format(previous_pred, previous_prey) + prado_para_str(meadow)) # primeiro display
    for i in range(num):
        meadow = geracao(meadow)
        if verbose:
            num_pred = obter_numero_predadores(meadow)
            num_prey = obter_numero_presas(meadow)
            if num_pred != previous_pred or num_prey != previous_prey: # apenas apresenta o display se houver uma alteração do número de predadores e/ou presas
                print("Predadores: {} vs Presas: {} (Gen. {})\n".format(num_pred, num_prey, i + 1) + prado_para_str(meadow)) # displays intermédios
                previous_pred = num_pred
                previous_prey = num_prey
    num_pred = obter_numero_predadores(meadow)
    num_prey = obter_numero_presas(meadow)
    if not verbose: # se não for escolhida a opção "verbose" é preciso apresentar o estado da última geração
        print("Predadores: {} vs Presas: {} (Gen. {})\n".format(num_pred, num_prey, num) + prado_para_str(meadow)) # último display
    return (num_pred, num_prey)