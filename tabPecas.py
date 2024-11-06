import sqlite3

# Conexão com o banco de dados
print('\033[1;34mConectando com o banco de dados...\033[m')
conector = sqlite3.connect("loja_pecas.db")
cursor = conector.cursor()
print('\033[1;32mConexão concluída.\033[m')

# Criação da tabela se ela não existir
try:
    sql = """
    create table pecas (
        codPeca integer primary key,
        descricao string,
        preco numeric not null,
        qtdeEstoque integer not null
        )
    """
    cursor.execute(sql)

except sqlite3.OperationalError:
    pass

# Loop enquanto o usuário quiser adicionar um produto
resp = 'S'
while resp == 'S':
    print('\033[1;35m-=' * 30)
    print(f'{'Informações do Produto:':^60}')
    print('-=' * 30, '\033[m')

    # Input dos dados pelo usuário
    try:
        # Validação de input do código do produto
        codPeca = -1
        while codPeca < 0:
            try:
                codPeca = int(input('Código do produto: '))
            except ValueError:
                print('\033[31mCódigo de tipo inválido ou nulo. Tente novamente.\033[m')
            else:
                if codPeca < 0:
                    print('\033[31mCódigo de tipo inválido. Tente novamente.\033[m')

        # A descrição pode ser nula, portanto não há necessidade de validação
        desc = str(input('Descrição: '))

        # Validação de input do preço do produto
        preco = 0
        while preco <= 0:
            try:
                preco = float(input('Preço: R$'))
            except ValueError:
                print('\033[31mFormato de preço inválido ou nulo. Tente novamente.\033[m')
            else:
                if preco <= 0:
                    print('\033[31mFormato de preço inválido. Tente novamente.\033[m')

        # Validação do input da quantidade de produtos em estoque
        qtde = 0
        while qtde <= 0:
            try:
                qtde = int(input('Quantidade em Estoque: '))
            except ValueError:
                print('\033[31mQuantidade inválida ou nula. Tente novamente.\033[m')
            else:
                if qtde <= 0:
                    print('\033[31mQuantidade inválida. Tente novamente.\033[m')

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
            insert into pecas values (?, ?, ?, ?)
        """
        param = [codPeca, desc, preco, qtde]
        cursor.execute(sql, param)
        conector.commit()
        print('\033[1;32mProduto registrado com sucesso.\033[m')

    except sqlite3.OperationalError:
        print('\033[31mErro ao registrar os dados.\033[m')

    # Caso uma chave primária tenha sido repetida
    except sqlite3.IntegrityError:
        print('\033[31mErro ao registrar os dados (valor de tipo único duplicado)\033[m')

    # Confirmação de loop para adicionar mais produtos
    resp = str(input('\033[1mDeseja adicionar outro produto? [S/N]: \033[m')).strip().upper()[0]
    while resp not in 'SN':
        print('\033[1;33mDigite sim (S) ou não (N) para continuar.\033[m')
        resp = str(input('\033[1mDeseja adicionar outro produto? [S/N]: \033[m')).strip().upper()[0]

# Fecha a conexão com o banco
cursor.close()
conector.close()

print()
print('\033[1;34mPrograma finalizado.\033[m')
