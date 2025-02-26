import sqlite3

# Conexão com o banco de dados
print('\033[1;34mConectando com o banco de dados...\033[m')
conector = sqlite3.connect("loja_pecas.db")
cursor = conector.cursor()
print('\033[1;32mConexão concluída.\033[m')

# Criação da tabela se ela não existir
try:
    sql = """
    create table pedidoItens (
        numPedido integer,
        codPeca integer,
        qtdePeca integer not null,
        subTotal numeric not null,
        primary key (numPedido, codPeca)
        )
    """
    cursor.execute(sql)

except sqlite3.OperationalError:
    pass

# Loop enquanto o usuário quiser adicionar um item por pedido
resp = 'S'
while resp == 'S':
    print('\033[1;35m-=' * 30)
    print(f'{'Informações do Pedido do Item:':^60}')
    print('-=' * 30, '\033[m')

    # Input dos dados pelo usuário
    try:
        # Validação de input do número do pedido
        numPedido = 0
        while numPedido <= 0:
            try:
                numPedido = int(input('Número do Pedido: '))
            except ValueError:
                print('\033[31mNúmero do pedido inválido ou nulo. Tente novamente.\033[m')
            else:
                if numPedido < 0:
                    print('\033[31mNúmero do pedido de tipo inválido. Tente novamente.\033[m')

        # Validação do código do item pedido
        codPeca = -1
        while codPeca < 0:
            try:
                codPeca = int(input('Código do produto: '))
            except ValueError:
                print('\033[31mCódigo de tipo inválido ou nulo. Tente novamente.\033[m')
            else:
                if codPeca < 0:
                    print('\033[31mCódigo de tipo inválido. Tente novamente.\033[m')

        # Validação da quantidade de itens do pedido
        qtde = 0
        while qtde <= 0:
            try:
                qtde = int(input('Quantidade: '))
            except ValueError:
                print('\033[31mQuantidade inválido ou nulo. Tente novamente.\033[m')
            else:
                if qtde < 0:
                    print('\033[31mQuantidade de tipo inválido. Tente novamente.\033[m')

        # Validação de input do subtotal do pedido
        subTotal = 0
        while subTotal <= 0:
            try:
                subTotal = float(input('Subtotal: R$'))
            except ValueError:
                print('\033[31mFormato de subtotal inválido ou nulo. Tente novamente.\033[m')
            else:
                if subTotal <= 0:
                    print('\033[31mFormato de subtotal inválido. Tente novamente.\033[m')

    # Caso o programa seja forçadamente finalizado durante o input, fecha o banco de dados e encerra o programa
    except KeyboardInterrupt:
        cursor.close()
        conector.close()
        print()
        print('\033[1;34mPrograma finalizado.\033[m')
        exit()

    # Inserção dos dados inputados pelo usuário no banco de dados
    try:
        sql = """
            insert into pedidoItens values (?, ?, ?, ?)
        """
        param = [numPedido, codPeca, qtde, subTotal]
        cursor.execute(sql, param)
        conector.commit()
        print('\033[1;32mPedido registrado com sucesso.\033[m')

    except sqlite3.OperationalError:
        print('\033[31mErro ao registrar os dados.\033[m')

    # Caso uma chave primária tenha sido repetida
    except sqlite3.IntegrityError:
        print('\033[31mErro ao registrar os dados (valor de tipo único duplicado)\033[m')

    # Confirmação de loop para adicionar mais produtos
    resp = str(input('\033[1mDeseja adicionar outro pedido? [S/N]: \033[m')).strip().upper()[0]
    while resp not in 'SN':
        print('\033[1;33mDigite sim (S) ou não (N) para continuar.\033[m')
        resp = str(input('\033[1mDeseja adicionar outro pedido? [S/N]: \033[m')).strip().upper()[0]

# Fecha a conexão com o banco
cursor.close()
conector.close()

print()
print('\033[1;34mPrograma finalizado.\033[m')
