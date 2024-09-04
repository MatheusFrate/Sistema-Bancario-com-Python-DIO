def valor_valido(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

def saque(*, saldo, limite, extrato, numero_saques, limite_saques):
    print('='.center(20, '='))
    print('Saque'.center(20))
    if numero_saques < limite_saques:  
        valor = input('Digite o valor do saque: ')
        if not valor_valido(valor):
            print("valor inválido, digite um número")
        else:
            valor = float(valor)
            if valor > limite:
                print('O sistema só permite saques de até R$ 500,00')
            elif valor <= 0:
                    print('Valor inválido, digite um valor maior que zero')
            elif valor > saldo:
                print('Saldo insuficiente')
            else:
                saldo = saldo - valor
                print(f'Saque realizado com sucesso, no valor de R$ {valor:.2f}')
                extrato.append(f'Saque -> valor: R${valor:.2f}')
                numero_saques += 1
                return saldo, extrato, numero_saques

    else:
        print('Limite de saques diários atingido')
    return saldo, extrato, numero_saques

def deposito(saldo, extrato):
    print('='.center(20, '=')) 
    print('Depósito'.center(20))
    valor = input('Digite o valor do depósito: ')
    if not valor_valido(valor):
        print("valor inválido, digite um número")
    else:
        valor = float(valor)
        if valor <= 0:
            print('Valor inválido, digite um valor maior que zero')
        else:
            saldo = saldo + valor
            print(f'Depósito realizado com sucesso, no valor de R$ {valor:.2f}')
            extrato.append(f'Deposito -> valor: R${valor:.2f}')
            return saldo, extrato
    return saldo, extrato

def extrato (saldo, /, *, extratos):
    print('='.center(20, '='))
    print('Extrato'.center(20))
    for item in extratos:
        print(item)
    print('-------------------')
    print(f'Saldo atual: R$ {saldo}')

def criar_usuario(usuarios):
    print('='.center(20, '='))
    print('Criar usuário'.center(20))
    nome = input('Digite o nome: ')
    data_nascimento = input('Digite a data de nascimento: ')
    cpf = input('Digite o CPF: ')
    endereco = input('Digite o endereço: ')
    if valor_valido(cpf):
        cpf = int(cpf)
        if cpf not in usuarios:
            usuarios[cpf] = {'nome': nome, 'data_nascimento': data_nascimento, 'endereco': endereco, 'saldo': 0}
            return usuarios
        else:
            print('CPF já cadastrado')
    else:
        print('CPF inválido')

def criar_conta(contas, proxima_conta):
    print('='.center(20, '='))
    print('Criar conta'.center(20))
    usuario = int(input('Digite o CPF: '))
    agencia = '0001'
    saldo = 0
    numero_saques = 0
    if usuario not in usuarios:
        print('Usuário não cadastrado')
    elif valor_valido(usuario):
        contas[proxima_conta] = {'agencia': agencia, 'saldo': saldo, 'limite': limite, 'numero_saques': numero_saques, 'limite_saques': LIMITE_SAQUES, 'usuario': usuario}
        return contas, proxima_conta + 1

def listar_usuarios(usuarios, contas):
    print('='.center(20, '='))
    print('Usuários'.center(20))
    for cpf, dados in usuarios.items():
        print(' Usuário '.center(20, '='))
        print(f'CPF: {cpf}')
        print(f'Nome: {dados["nome"]}')
        print(f'Data de nascimento: {dados["data_nascimento"]}')
        print(f'Endereço: {dados["endereco"]}')
        print(f'Saldo: {dados["saldo"]}')
        print(' Contas '.center(20, '='))
        for conta in contas:
            if contas[conta]['usuario'] == cpf:
                print(f'Conta: {conta}')
                print(f'Agência: {contas[conta]["agencia"]}')
                print(f'Saldo: {contas[conta]["saldo"]}')
                print(f'Limite: {contas[conta]["limite"]}')
                print(f'Número de saques: {contas[conta]["numero_saques"]}')
                print(f'Limite de saques: {contas[conta]["limite_saques"]}')
                print('-------------------')

        print('-------------------')

def menu():
    return """
    [d] - Depositar
    [s] - Sacar
    [e] - Extrato
    [u] - Criar usuário
    [c] - Criar conta
    [l] - Listar usuários
    [x] - Sair
""" 


saldo = 0
limite = 500
extratos = []
usuarios = {1: {'nome': 'João', 'data_nascimento': '01/01/2000', 'endereco': 'Rua A', 'saldo': 0}}
contas = {1: {'agencia': '0001', 'saldo': 0, 'limite': 500,'numero_saques':0, 'limite_saques': 3, 'usuario':1}}
proxima_conta = 2
numero_saques = 0
LIMITE_SAQUES = 3 # limite de saques diários - Constante

while True:

    opcao = input(menu()).lower()
    
    if opcao == 'd':
        saldo, extratos = deposito(saldo, extratos)
    
    elif opcao == 's':
        saldo, extratos, numero_saques = saque(saldo=saldo, limite=limite, extrato=extratos, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
            
    elif opcao == 'e':
        extrato(saldo, extratos=extratos)

    elif opcao == 'u':
       
        usuarios = criar_usuario(usuarios)

    elif opcao == 'c':
        
        contas, proxima_conta = criar_conta(contas, proxima_conta)
    
    elif opcao == 'l':
        listar_usuarios(usuarios, contas)

    elif opcao == 'x':
        print('Até logo!')
        break
    else: 
        print('Opção inválida!')
