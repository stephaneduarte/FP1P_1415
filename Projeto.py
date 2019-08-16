#81186 - Stephane Duarte

#Este programa permite verificar o numero de cartoes de credito, identificando a categoria da entidade que emitiu o cartao e a respetiva rede emissora. Permite ainda gerar novos numeros de cartao de credito.

#Importa a funcao random
import random

#Entidades emissoras, digitos iniciais, possiveis tamanhos do numero e respetiva sigla
EE = (("American Express", ("34", "37"), (15,), "AE"),
       ("Diners Club International", ("309", "36", "38", "39"), (14,), "DCI"),
       ("Discover Card", ("65",), (16,), "DC"),
       ("Maestro", ("5018", "5020", "5038"), (13,19), "M"),
       ("Master Card", ("50", "51", "52", "53", "54", "19"), (16,), "MC"),
       ("Visa Electron",("4026", "426", "4405", "4508"), (16,), "VE"),
       ("Visa",("4024", "4532", "4556"), (13,16), "V"))

#categoria da entidade que emite o cartao reconhecida atraves do primeiro digito do numero
ENT = (("Companhias aereas", ("1",)),
       ("Companhias aereas e outras tarefas futuras da industria", ("2",)),
       ("Viagens e entretenimento e bancario / financeiro", ("3",)),
       ("Servicos bancarios e financeiros", ("4","5")),
       ("Merchandising e bancario / financeiro", ("6",)),
       ("Petroleo e outras atribuicoes futuras da industria", ("7",)),
       ("Saude, telecomunicacoes e outras atribuicoes futuras da industria", ("8",)),
       ("Atribuicao nacional", ("9",)))
    
def calc_soma(n):
    #a funcao calc_soma recebe uma cadeia de caracteres e devolve um inteiro
    """A funcao devolve a soma ponderada dos digitos de n, calculada de acordo com o algoritmo de Luhn."""
    inv = ''
    soma = 0
    for i in range(len(n)-1, -1, -1):
        inv = inv + n[i] #inverte o numero
    for i in range(0, len(inv)):
        a = eval(inv[i])
        if i % 2 != 0: #se a posicao for par
            soma = soma + a
        else: #se a posicao for impar
            a = a * 2
            if a > 9:
                a = a - 9
            soma = soma + a
    return soma #inteiro calculado pelo algoritmo de Luhn


def luhn_verifica(nr_cc):
    #A funcao recebe uma cadeia de caracteres e devolve True ou False
    """Devolve True se o numero passar o algoritmo de Luhn, e False em caso contrario."""
    
    nr_cs = str(eval(nr_cc) // 10)
    soma_i = calc_soma(nr_cs) #soma incompleta sem o check digit
    cd = eval(nr_cc) % 10 #guarda o check digit
    soma_c = soma_i + cd
    if soma_c % 10 == 0:
        return True
    else:
        return False


def comeca_por(cad1, cad2):
    """Valida se o primeiro numero inserido comeca pelo segundo numero inserido."""
    #a funcao recebe duas cadeias de caracteres e retorna True se o tamanho do primeiro numero for maior ou igual ao do segundo e a cad1 comecar por cad2
    return len(cad1) >= len(cad2) and cad1[:len(cad2)] == cad2

def comeca_por_um(cad, t_cads):
    """Valida se o primeiro numero inserido comeca por um dos elementos do tuplo colocado em segundo lugar."""
    #a funcao rece uma cadeia de caracteres e um tuplo e retorna True se cad1 comecar por um dos elementos do tuplo t_cads
    for elem in t_cads:
        if comeca_por(cad, elem):
            return True
    return False

def valida_iin(nm_cc):
    """Devolve o nome da rede emissora do cartao correspondente ao numero inserido, caso exista."""
    #a funcao recebe uma cadeia de caracteres e devolve uma cadeia de caracteres
    for tipo in EE: #tuplo das entidades emissoras
        if len(nm_cc) in tipo[2] and comeca_por_um(nm_cc,tipo[1]):
            return tipo[0]
    return ''
    
def categoria(nm_cc):
    """Devolve o nome da categoria da entidade correspondente ao primeiro digito do numero de cartao de credito"""
    #a funcao recebe uma cadeia de caracteres e devolve uma cadeia de caracteres ou uma mensagem de erro se o primeiro digito nao corresponder a qualquer categoria
    for tipo in ENT: #tuplo das categorias das entidades emissoras
        if nm_cc[0] in tipo[1]:
            return tipo[0]
    raise ValueError("O numero inserido nao e um numero de cartao de credito.")
        

def verifica_cc(n):
    '''A funcao verifica a validade de um numero de cartao de credito.'''
    #a funcao recebe um inteiro correspondente ao numero de um cartao de credito e devolve a categoria do cartao e o nome da rede emissora, caso o numero seja valido
    n = str(n)
    if valida_iin(n) != '':
        if luhn_verifica(n): #valida o algoritmo de luhn
            return (categoria(n), valida_iin(n))
        else:
            return 'cartao invalido'
    else:
        return 'cartao invalido'
    
def preftam(abr):
    """Atribui um prefixo e um tamanho ao numero de cartao de credito desejado."""
    #recebe uma cadeia de caracteres e devolve um tuplo (prefixo, tamanho)
    for tipo in EE:
        if abr == tipo[3]:
            return (tipo[1][int(random.random()*len(tipo[1]))], tipo[2][int(random.random()*(len(tipo[2])))])
        #a funcao random vai gerar valores aleatorios de [0, 1[, que multiplicados pelo tamanho de um tuplo, geram valores de [0, tamanho do tuplo[
        #depois acede a posicao do inteiro do valor gerado no respetivo tuplo
    raise ValueError("A abreviatura nao corresponde a nenhuma rede emissora.")

def numscd(abr):
    """Adiciona ao prefixo um conjunto de numeros ate satisfazer o tamanho desejado sem o check digit"""
    #a funcao recebe uma cadeia de caracteres e devolve uma cadeia de caracteres 
    pref = preftam(abr)[0]
    tam = preftam(abr)[1] #tamanho com o check digit
    numscd = eval(pref)
    while len(str(numscd)) < (tam-1): #enquanto o tamanho nao corresponder ao tamanho pretendido sem o check digit
        numscd = numscd * 10 + int(random.random()*10)
    return str(numscd)

def digito_verificacao(numscd):
    """Calcula o check digit de um numero de cartao de credito"""
    #a funcao recebe cadeia de caracteres e devolve uma cadeia de caracteres
    soma = calc_soma(numscd)
    if soma % 10 == 0: #se a soma for um multiplo de 10 o CD e 0.
        return '0'
    else: #se a soma nao for multiplo de dez
        a = soma // 10
        a = (a + 1)*10
        cd = a - soma #subtrai-se o valor da soma ao multiplo de dez exatamente a seguir
        return str(cd)
    
def gera_num_cc(abr):
    #a funcao recebe uma cadeia de caracteres e devolve um inteiro correspondente ao numero gerado
    inicio = numscd(abr) #obtem o inicio do numero do cartao de credito
    cd = digito_verificacao(inicio)
    inicio = eval(inicio) * 10 #transforma-o num inteiro e multiplica por 10
    cd = eval(cd)
    return inicio + cd