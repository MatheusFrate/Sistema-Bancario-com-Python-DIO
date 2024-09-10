from abc import ABC, abstractmethod
from datetime import datetime

 
class Cliente:
    def __init__ (self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)      

class PessoaFisica (Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        if valor <= 0:
            print('\nValor inválido, digite um valor maior que zero\n')
            print('@'*50)
        elif valor > saldo:
            print('\nSaldo insuficiente\n')
            print('@'*50)
        else:
            print(f'\nSaque realizado com sucesso, no valor de R$ {valor:.2f}\n')
            print('='*50)
            self._saldo -= valor
            return True
        return False
    
    def depositar(self, valor):
        if valor <= 0:
            print('\nValor inválido, digite um valor maior que zero\n')
            print('@'*50)
        else:
            print(f'\nDepósito realizado com sucesso, no valor de R$ {valor:.2f}\n')
            print('='*50)
            self._saldo += valor
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, numero,cliente, limite_saques = 3, limite = 500):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):

        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__ and transacao['status'] == True])

        if self.limite_saques > numero_saques:  
            if not self.valor_valido(valor):
                print("\nvalor inválido, digite um número\n")
                print('@'*50)
            valor = float(valor)
            if valor > self.limite:
                print(f'\nO sistema só permite saques de até R$ {self.limite:.2f}\n')
                print('@'*50)
            
            else:
                return super().sacar(valor)
        else:
            print('\nLimite de saques diários atingido\n')
            print('@'*50)
        return False

    def depositar(self, valor):
        if not self.valor_valido(valor):
            print("\nvalor inválido, digite um número\n")
            print('@'*50)
        else:
            valor = float(valor)
            return super().depositar(valor)
        return False

    def valor_valido(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False
        
    def __str__(self):
        return f"""
            agencia:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
         """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'status': transacao.status,
            'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        })

class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @property
    @abstractmethod
    def status(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._status = False

    @property
    def valor(self):
        return self._valor
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, valor):
        self._status = valor
    
    def registrar(self, conta):
        self.status = conta.sacar(self.valor)        
        conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._status = False

    @property
    def valor(self):
        return self._valor

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, valor):
        self._status = valor
    
    def registrar(self, conta):
        self.status = conta.depositar(self.valor)
        conta.historico.adicionar_transacao(self)

class Menu:
    clientes = [PessoaFisica('João', '01/01/1990', '1', 'Rua A')]
    contas = [
        ContaCorrente(1, clientes[0])
    ]
    clientes[0].adicionar_conta(contas[0])
    proxima_conta = 1
    def menu(self):
        return """
            [d] - Depositar
            [s] - Sacar
            [e] - Extrato
            [u] - Criar Usuário
            [c] - Criar Conta
            [l] - Listar Usuários
            [x] - Sair
            """

    def filtrar_cliente(self, cpf):
        clientes_filtrados = [cliente for cliente in self.clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None
    
    def recuperar_conta_cliente(self, cliente):
        #fixme: verificar se o cliente possui mais de uma conta, e permitir escolha
        if cliente.contas:
            return cliente.contas[0]
        else:
            print('Cliente não possui conta em seu nome!')
            return 

    def  depositar(self):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print('Cliente não encontrado!')
            return
        
        valor = (input("Digite o valor a ser depositado:"))
        transacao = Deposito(valor)
        conta = self.recuperar_conta_cliente(cliente)

        if not conta:
            return
        
        cliente.realizar_transacao(conta, transacao)

    def sacar(self):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print('Cliente não encontrado!')
            return

        valor = (input("Digite o valor a ser sacado:"))
        transacao = Saque(valor)
        conta = self.recuperar_conta_cliente(cliente)

        if not conta:
            return
        
        cliente.realizar_transacao(conta, transacao)

    def exibir_extrato(self):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print('Cliente não encontrado!')
            return
        
        conta = self.recuperar_conta_cliente(cliente)

        extrato = conta.historico.transacoes
        print('='.center(50, '='))
        print('Extrato'.center(50))
        for itens in extrato:
            print(f'Tipo: {itens["tipo"]} \n Valor: {itens["valor"]} \n Data: {itens["data"]}, \n Status: {itens["status"]}')
            print('-'*50)

        print(f'Saldo atual: R$ {conta.saldo:.2f}')
        print('='.center(50, '='))

    def criar_cliente(self):
        cpf = input('Digite o CPF: ')
        cliente = self.filtrar_cliente(cpf)

        if cliente:
            print('Cliente já cadastrado!')
            return
        
        nome = input('Digite o nome: ')
        data_nascimento = input('Digite a data de nascimento: ')
        endereco = input('Digite o endereço: ')

        cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
        self.clientes.append(cliente)
        print('Cliente cadastrado com sucesso!')

    def criar_conta(self):
        cpf = input('Digite o CPF do cliente: ')
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print('Cliente não encontrado!')
            return

        numero = self.proxima_conta
        conta = ContaCorrente.nova_conta(cliente = cliente, numero = numero)
        cliente.adicionar_conta(conta)
        self.contas.append(conta)
        print(f'Conta criada com sucesso! Número da conta: {numero}')

    def listar_contas(self):
        print("=" * 50)
        for conta in self.contas:
            print(conta)
            print("=" * 50)

    def main(self):
        while True:
            print(self.menu())
            opcao = input('Digite a opção desejada: ')

            if opcao == 'd':
                self.depositar()

            elif opcao == 's':
                self.sacar()

            elif opcao == 'e':
                self.exibir_extrato()
            
            elif opcao == 'u':
                self.criar_cliente()

            elif opcao == 'c':
                self.criar_conta()

            elif opcao == 'l':
                self.listar_contas()
            
            elif opcao == 'x':
                print('Saindo...')
                break

Menu().main()
