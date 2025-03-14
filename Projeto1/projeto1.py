#99951 Guilherme Leitão

'''Este script contém as funções desenvolvidas com o intuito de identificar, corrigir e filtrar
   determinadas informações relacionadas com utilizadores da base de dados BDB que se encontram
   corrompidas.
   
   Assim, primeiramente, é corrigida a documentação crucial para a desencriptação dos dados da base.
   Após a obtenção da documentação, passa-se à fase de descoberta do pin de desbloqueio da BDB.
   Posteriormente, é feita uma primeira verificação dos dados (possivelmente corrompidos) e apenas
   depois se passa à desencriptação destes. Finalmente, para último fica a depuração das senhas
   associadas a contas que tiveram a sua informação corrompida.
   
   Diga NÃO à pirataria informática :)'''

def corrigir_palavra(word):
    # cad. carateres -> cad. carateres
    '''Recebe uma cadeia de carateres que representa uma palavra possivelmente
       modificada e corrige-a de acordo com a sequência de reduções maiúscula <-> minúscula,
       e vice-versa, especificada no problema, devolvendo-a corrigida'''
    previous_letter = "."
    i = 0
    while i < len(word):
        for l in word:
            # se houver duas letras iguais consecutivas, uma maiúscula e a outra minúscula
            if ((l.islower() and previous_letter.isupper() or l.isupper() and previous_letter.islower())\
                and l.isalpha() and previous_letter.isalpha()) and l.lower() == previous_letter.lower():
                word = word.replace(previous_letter + l, "")
                previous_letter = "."
                i = 0
                break
            previous_letter = l
            i += 1
    return word


def eh_anagrama(word1, word2):
    # cad. carateres x cad. carateres -> booleano
    '''Recebe duas cadeias de carateres representando cada uma palavra e devolve True
       se e só se uma for um anagrama da outra, ignorando maiúsculas e minúsculas'''
    # ignora se é carater maiúsculo ou minúsculo
    word1 = word1.lower()
    word2 = word2.lower()
    map1 = {}
    map2 = {}
    for l in word1:
        if map1.get(l) == None:
            map1.update({l:1})
        else:
            map1.update({l:map1.get(l) + 1})
    for l in word2:
        if map2.get(l) == None:
            map2.update({l:1})
        else:
            map2.update({l:map2.get(l) + 1})
    return map1 == map2


def corrigir_doc(phrase):
    # cad. carateres -> cad. carateres
    '''Recebe uma cadeia de carateres à qual aplica o processo de filtração desenvolvido
       anteriormente - maiúscula <-> minúscula, e vice-versa, e remoção dos anagramas diferentes
       da palavra - e devolve a sua correção'''
    # apenas deve ser constituido por palavras separadas por um único espaço
    if not isinstance(phrase, str) or phrase.find("  ") != -1:
        raise ValueError("corrigir_doc: argumento invalido")
    words = phrase.split(" ")
    phrase = ""
    # corrige as palavras de acordo com os pares de letras maiúscula - minúscula (<->)
    for i in range(len(words)):
        if not words[i].isalpha():
            raise ValueError("corrigir_doc: argumento invalido")
        words[i] = corrigir_palavra(words[i])
    i = 0
    # retira os anagramas diferentes da frase
    while i < len(words):
        for j in range(i):
            if eh_anagrama(words[i], words[j]) and not (words[i].lower() == words[j].lower()):
                words.pop(i)
                i = 0
                break
        i += 1
    for word in words:
        phrase += word + " "
    # remove o último espaço que permanece por default
    phrase = phrase.rstrip(" ")
    return phrase


def obter_posicao(move, pos):
    # cad. carateres x inteiro -> inteiro
    '''Recebe um carater que representa o movimento a efetuar - Esquerda, Direita,
       Baixo e Cima - e uma posição inicial no painel de dígitos e devolve a posição
       resultante após a prática do respetivo movimento'''
    # aqui dá-se a definição do conceito de painel de dígitos
    panel = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    row = 0
    col = 0
    # descoberta da linha e coluna da posição incial
    for i in range(3):
        for j in range(3):
            if panel[i][j] == pos:
                row = i
                col = j
    # deslocação para cima no painel
    if move == "C":
        if row - 1 < 0:
            return panel[row][col]
        return panel[row - 1][col]
    # deslocação para baixo no painel
    if move == "B":
        if row + 1 > 2:
            return panel[row][col]
        return panel[row + 1][col]
    # deslocação para a esquerda no painel
    if move == "E":
        if col - 1 < 0:
            return panel[row][col]
        return panel[row][col - 1]
    # deslocação para a direita no painel
    if move == "D":
        if col + 1 > 2:
            return panel[row][col]
        return panel[row][col + 1]


def obter_digito(seq, pos):
    # cad. carateres x inteiro -> inteiro
    '''Recebe uma cadeia de carateres representando uma sequência de um ou mais
       movimentos descritos acima e uma posição inicial no painel de dígitos 
       e devolve a posição final neste mesmo painel após a execução da dita sequência'''
    for l in seq:
        pos = obter_posicao(l, pos)
    return pos


def obter_pin(key):
    # tuplo -> tuplo
    '''Recebe um tuplo de sequências a realizar sobre um dado painel de dígitos, 
       tendo como posição inicial o botão '5' e devolve um tuplo de inteiros 
       representando as posições após o efetuar dos respetivos movimentos'''
    if not isinstance(key, tuple) or len(key) < 4 or len(key) > 10:
        raise ValueError("obter_pin: argumento invalido")
    final_key = ()
    dig = 5
    # para cada sequência, performa as respetivas deslocações
    for seq in key:
        if not isinstance(seq, str) or not seq:
            raise ValueError("obter_pin: argumento invalido")
        for l in seq:
            if l != "E" and l != "D" and l != "C" and l != "B":
                raise ValueError("obter_pin: argumento invalido")
        dig = obter_digito(seq, dig)
        final_key += (dig,)
    return final_key


def eh_entrada(entry):
    # universal -> booleano
    '''Recebe um qualquer argumento e devolve True se e só se este corresponda
       a uma entrada da BDB, isto é, um tuplo com uma cifra, uma sequência de controlo
       e uma sequência de segurança'''
    if not isinstance(entry, tuple) or len(entry) != 3 or not isinstance(entry[0], str)\
       or not isinstance(entry[1], str) or not isinstance(entry[2], tuple):
        return False
    # repartição da cifra em palavras individuais
    cifra = entry[0].split("-")
    for word in cifra:
        if not word:    #if empty string
            return False
        for l in word:
            if not l.isalpha() or l.isupper():
                return False
    if len(entry[1]) != 7 or entry[1][0] != "[" or entry[1][6] != "]" or\
       not entry[1][1:6].isalpha() or not entry[1][1:6].islower():
        return False
    if len(entry[2]) < 2:
        return False
    for num in entry[2]:
        if not isinstance(num, int) or num <= 0:
            return False
    letter_map = {}
    for l in entry[0]:
        letter_map.update({l:0})
    if len(letter_map) < 6:
        return False
    return True


def validar_cifra(cifra, seq):
    # cad. carateres x cad. carateres -> booleano
    '''Recebe duas cadeias de carateres representando uma cifra e uma sequência de control,
       respetivamente, e devolve True se e só se a sequência de controlo é compativel com a
       respetiva cifra, de acordo com o problema'''
    letter_map = {}
    cifra = cifra.split("-")
    for word in cifra:
        for l in word:
            if letter_map.get(l) == None:
                letter_map.update({l : 1})
            else:
                letter_map.update({l : letter_map.get(l) + 1})
    seq = seq.strip("[]")
    # repete apenas 5 vezes pois a sequência de controlo deve conter apenas 5 carateres
    for i in range(5):
        for l in letter_map:
            if letter_map.get(seq[i]) == None:
                return False
            if letter_map.get(seq[i]) <= letter_map.get(l) and seq[i] != l:
                if letter_map.get(seq[i]) < letter_map.get(l) or ord(seq[i]) > ord(l):
                    return False
        letter_map.pop(seq[i])
    return True


def filtrar_bdb(bdb):
    # lista -> lista
    '''Recebe uma lista representando uma ou mais entradas da BDB e devolve apenas
       as entradas que não estão de acordo com a relação cifra <-> sequência de controlo
       explicada no enunciado'''
    if not isinstance(bdb, list) or len(bdb) == 0:
        raise ValueError("filtrar_bdb: argumento invalido")
    report_bdb = []
    # para cada entrada da BDB, avalia se essa está de acordo com a relação acima descrita
    for entry in bdb:
        if not eh_entrada(entry):
            raise ValueError("filtrar_bdb: argumento invalido")
        if not validar_cifra(entry[0], entry[1]):
            report_bdb.append(entry)
    return report_bdb


def obter_num_seguranca(security_seq):
    # tuplo -> inteiro
    '''Recebe um tuplo de inteiros representando a sequência de segurança e devolve o menor valor
       de todas as diferenças entre todos os valores do tuplo, ou seja, o número de segurança'''
    diff = ()
    for i in range(1, len(security_seq)):
        for j in range(i):
            diff += (abs(security_seq[i] - security_seq[j]),)
    return min(diff)


def decifrar_texto(cifra, security_num):
    # cad. carateres x inteiro -> cad. carateres
    '''Recebe uma cadeia de carateres - cifra - e um número de segurança e devolve uma cadeia
       de carateres que representa a mesma cifra decifrada conforme explicado no problema'''
    deciphered = ""
    security_num = security_num % 26
    for i in range(len(cifra)):
        if cifra[i] == "-":
            deciphered += " "
        else:
            # se for correspondente a uma posição par
            if i % 2 == 0:
                # se a deslocação implicar "ultrapassar" o carater "z"
                if ord(cifra[i]) + security_num > 121:
                    deciphered += chr(ord(cifra[i]) + security_num - 25)
                else:
                    deciphered += chr(ord(cifra[i]) + security_num + 1)
            else:
                if ord(cifra[i]) + security_num > 123:
                    deciphered += chr(ord(cifra[i]) + security_num - 27)
                else:
                    deciphered += chr(ord(cifra[i]) + security_num - 1)
    return deciphered


def decifrar_bdb(bdb):
    # lista -> lista
    '''Recebe uma lista contendo uma ou mais entradas da BDB e devolve uma lista contendo
       apenas as respetivas cifras decifradas pelo algoritmo acima descrito'''
    if not isinstance(bdb, list) or len(bdb) == 0:
        raise ValueError("decifrar_bdb: argumento invalido")
    deciphered_bdb = []
    for entry in bdb:
        if not eh_entrada(entry):
            raise ValueError("decifrar_bdb: argumento invalido")
        deciphered_bdb.append(decifrar_texto(entry[0], obter_num_seguranca(entry[2])))
    return deciphered_bdb


def eh_utilizador(data):
    # universal -> booleano
    '''Recebe um argumento e retorna True se e só se este for um dicionário correspondente
       à informação de um utilizador da BDB, com um nome, senha e regra individual, descritas
       no enunciado'''
    if not isinstance(data, dict) or len(data) != 3 or data.get("name") == None\
       or data.get("pass") == None or data.get("rule") == None:
        return False
    if not isinstance(data.get("name"), str) or not isinstance(data.get("pass"), str)\
       or len(data.get("name")) < 1 or len(data.get("pass")) < 1 or not isinstance(data.get("rule"), dict):
        return False
    rule = data.get("rule")
    if len(rule) != 2 or rule.get("vals") == None or rule.get("char") == None:
        return False
    if not isinstance(rule.get("vals"), tuple) or len(rule.get("vals")) != 2\
       or not isinstance(rule.get("char"), str) or len(rule.get("char")) != 1\
       or not (rule.get("char").isalpha() and rule.get("char").islower()):
        return False
    dig1 = rule.get("vals")[0]
    dig2 = rule.get("vals")[1]
    if not isinstance(dig1, int) or not isinstance(dig2, int) or dig1 <= 0 or dig2 <= 0 or dig2 < dig1:
        return False
    return True


def eh_senha_valida(passwd, rule):
    # cad. carateres x dicionário -> booleano
    '''Recebe uma cadeia de carateres correspondente a uma senha e um dicionário correspondente a
       uma regra individual e devolve True se e só se a senha respeitar as regras gerais e
       respetiva individual'''
    # se houver menos que três vogais minúsculas
    if passwd.count("a") + passwd.count("e") + passwd.count("i") + passwd.count("o") + passwd.count("u") < 3:
        return False
    # se não houver duas letras iguais consecutivas
    repeated_char = False
    previous_char = ""
    for l in passwd:
        if l == previous_char:
            repeated_char = True
            break
        previous_char = l
    if not repeated_char:
        return False
    min = rule.get("vals")[0]
    max = rule.get("vals")[1]
    num_x = passwd.count(rule.get("char"))
    # se o intervalo não estiver bem definido
    if num_x < min or num_x > max:
        return False
    return True


def filtrar_senhas(data):
    # lista -> lista
    '''Recebe uma lista que corresponde a uma ou mais entradas da BDB com a informação
       dos utilizadores e retorna uma lista com os nomes dos utilizadores com senhas errdas
       por ordem alfabética'''
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("filtrar_senhas: argumento invalido")
    filtered_data = []
    for user_info in data:
        if not eh_utilizador(user_info):
            raise ValueError("filtrar_senhas: argumento invalido")
        # se a senha não for válida de acordo com os critérios acima definidos
        if not eh_senha_valida(user_info.get("pass"), user_info.get("rule")):
            filtered_data.append(user_info.get("name"))
    # organização dos nomes requeridos por ordem alfabética
    filtered_data.sort()
    return filtered_data