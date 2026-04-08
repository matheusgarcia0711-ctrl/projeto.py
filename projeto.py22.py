import random
import datetime

def menu():
    nome_arq = 'log.txt'

    while True:
        print('\nMENU')
        print('1 - Gerar logs')
        print('2 - Analisar logs')
        print('3 - Gerar e analisar logs')
        print('4 - Sair')

        opc = input('Digite a opção desejada: ')

        if opc == '1':
            qtd = int(input('Quantidade de logs: '))
            gerarArquivo(nome_arq, qtd)

        elif opc == '2':
            analisarLogs(nome_arq)

        elif opc == '3':
            qtd = int(input('Quantidade de logs: '))
            gerarArquivo(nome_arq, qtd)
            analisarLogs(nome_arq)

        elif opc == '4':
            print('Até mais!')
            break

        else:
            print('Opção inválida!')



def gerarArquivo(nome_arq, qtd):
    with open(nome_arq, 'w') as arq:
        for i in range(qtd):
            arq.write(montarLog(i) + '\n')
    print('Logs gerados com sucesso!')


def montarLog(i):
    data = gerarData(i)
    ip = gerarIp(i)
    recurso = gerarRecurso(i)
    metodo = gerarMetodo(i)
    status = gerarStatus(i)
    tempo = gerarTempo(i)
    agente = gerarAgente(i)
    tamanho = gerarTamanho(i)
    protocolo = gerarProtocolo(i)

    return f'[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - {tamanho} - {protocolo} - {agente} - /home'


def gerarData(i):
    base = datetime.datetime.now()
    delta = datetime.timedelta(seconds=i * random.randint(5, 20))
    return (base + delta).strftime('%d/%m/%Y %H:%M:%S')


def gerarIp(i):
    if 20 <= i <= 50:
        return '203.120.45.7'
    return '192.168.1.' + str(random.randint(1, 10))


def gerarRecurso(i):
    if i % 5 == 0:
        return '/admin'
    elif i % 3 == 0:
        return '/login'
    else:
        return '/home'


def gerarMetodo(i):
    return 'GET'


def gerarStatus(i):
    if i % 10 == 0:
        return '500'
    elif i % 3 == 0:
        return '403'
    elif i % 4 == 0:
        return '404'
    else:
        return '200'


def gerarTempo(i):
    return random.randint(100, 1000)


def gerarAgente(i):
    if i % 7 == 0:
        return 'Bot'
    return 'Chrome'


def gerarTamanho(i):
    return str(random.randint(200, 1000)) + 'B'


def gerarProtocolo(i):
    return 'HTTP/1.1'



def extrairStatus(linha):
    cont = 0
    status = ''
    i = 0

    while i < len(linha):
        if linha[i] == '-':
            cont += 1
            i += 2
            if cont == 2:
                while linha[i] != ' ':
                    status += linha[i]
                    i += 1
                return status
        i += 1
    return status


def extrairTempo(linha):
    cont = 0
    tempo = ''
    i = 0

    while i < len(linha):
        if linha[i] == '-':
            cont += 1
            i += 2
            if cont == 4:
                while linha[i] != 'm':
                    tempo += linha[i]
                    i += 1
                return int(tempo)
        i += 1
    return 0


def extrairIP(linha):
    ip = ''
    i = 0

    while linha[i] != ']':
        i += 1
    i += 2

    while linha[i] != ' ':
        ip += linha[i]
        i += 1

    return ip


def extrairRecurso(linha):
    cont = 0
    recurso = ''
    i = 0

    while i < len(linha):
        if linha[i] == '-':
            cont += 1
            i += 2
            if cont == 3:
                while linha[i] != ' ':
                    recurso += linha[i]
                    i += 1
                return recurso
        i += 1
    return recurso


def classificarTempo(tempo):
    if tempo < 200:
        return 'rapido'
    elif tempo < 800:
        return 'normal'
    else:
        return 'lento'



def analisarLogs(nome_arq):
    arquivo = open(nome_arq, 'r')

    total = 0
    sucesso = 0
    erro = 0
    erro500 = 0

    soma_tempo = 0
    maior_tempo = 0
    menor_tempo = 999999

    rapidos = 0
    normais = 0
    lentos = 0

    cont_500 = 0
    falha_critica = 0

    anterior = 0
    cont_crescendo = 0
    degradacao = 0

    ip_anterior = ''
    cont_ip = 0
    bots = 0

    for linha in arquivo:
        total += 1

        status = extrairStatus(linha)
        tempo = extrairTempo(linha)
        ip = extrairIP(linha)

        soma_tempo += tempo

        if tempo > maior_tempo:
            maior_tempo = tempo

        if tempo < menor_tempo:
            menor_tempo = tempo

        tipo = classificarTempo(tempo)

        if tipo == 'rapido':
            rapidos += 1
        elif tipo == 'normal':
            normais += 1
        else:
            lentos += 1

        if status == '200':
            sucesso += 1
        else:
            erro += 1

        if status == '500':
            erro500 += 1
            cont_500 += 1
        else:
            cont_500 = 0

        if cont_500 == 3:
            falha_critica += 1

        if tempo > anterior:
            cont_crescendo += 1
        else:
            cont_crescendo = 0

        if cont_crescendo == 3:
            degradacao += 1

        anterior = tempo

        if ip == ip_anterior:
            cont_ip += 1
        else:
            cont_ip = 1

        if cont_ip == 5:
            bots += 1

        ip_anterior = ip

    arquivo.close()

    media = soma_tempo / total
    disponibilidade = (sucesso / total) * 100
    taxa_erro = (erro / total) * 100

    if falha_critica > 0 or disponibilidade < 70:
        estado = 'CRITICO'
    elif disponibilidade < 85:
        estado = 'INSTAVEL'
    elif disponibilidade < 95:
        estado = 'ATENCAO'
    else:
        estado = 'SAUDAVEL'

    print('\n===== RELATORIO =====')
    print('Total de acessos:', total)
    print('Sucessos:', sucesso)
    print('Erros:', erro)
    print('Erros 500:', erro500)

    print('Disponibilidade:', disponibilidade)
    print('Taxa de erro:', taxa_erro)

    print('Tempo medio:', media)
    print('Maior tempo:', maior_tempo)
    print('Menor tempo:', menor_tempo)

    print('Rapidos:', rapidos)
    print('Normais:', normais)
    print('Lentos:', lentos)

    print('Falhas criticas:', falha_critica)
    print('Degradacao:', degradacao)
    print('Bots:', bots)