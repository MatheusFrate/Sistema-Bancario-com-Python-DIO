menu = """
    [d] - Depositar
    [s] - Sacar
    [e] - Extrato
    [x] - Sair
"""

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3 # limite de saques diários - Constante

while True:

    opcao = input(menu).lower()

    if opcao == 'd':
        print('='.center(200, '=')) # centraliza o texto
        print('Depósito'.center(20))
        valor = input('Digite o valor do depósito: ')
        if not valor.isnumeric():
            print('Valor inválido, digite um número')
        elif valor <= 0:
            print('Valor inválido, digite um valor maior que zero')
        else:
            saldo = saldo + valor
            print(f'Depósito realizado com sucesso, no valor de R$ {valor:.2f}')
            extrato.append(f'Deposito -> valor: R${valor:.2f}')
    
    elif opcao == 's':
        print('====================')
        print('Saque'.center(20))
        if numero_saques < LIMITE_SAQUES:  
            valor = float(input('Digite o valor do saque: '))
            if valor > limite:
                print('O sistema só permite saques de até R$ 500,00')
            elif valor > saldo:
                print('Saldo insuficiente')
            else:
                saldo = saldo - valor
                numero_saques += 1
                print(f'Saque realizado com sucesso no valor de R$ {valor:.2f}')
                extrato.append(f'Saque -> valor: R${valor:.2f}')
        else:
            print('Limite de saques diários atingido')
            
    elif opcao == 'e':
        print('====================')
        print('Extrato'.center(20))
        for item in extrato:
            print(item)
        print('-------------------')
        print(f'Saldo atual: R$ {saldo}')

    elif opcao == 'x':
        print('Até logo!')
        break

    else: 
        print('Opção inválida!')