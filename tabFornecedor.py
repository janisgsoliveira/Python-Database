import sqlite3

# Conexão com o banco de dados
print('\033[1;34mConectando com o banco de dados...\033[m')
conector = sqlite3.connect("loja_pecas.db")
cursor = conector.cursor()
print('\033[1;32mConexão concluída.\033[m')

# Criação da tabela se ela não existir
try:
    sql = """
        create table fornecedor (
            codInterno integer primary key,
            razaoSiocial string not null,
            nomeFantasia string not null,
            CNPJ string not null,
            endereco string,
            telCentral string not null
            )
        """
    cursor.execute(sql)

except sqlite3.OperationalError:
    pass

# Loop enquanto o usuário quiser adicionar um fornecedor
resp = 'S'
while resp == 'S':
    print('\033[1;35m-=' * 30)
    print(f'{'Informações do Produto:':^60}')
    print('-=' * 30, '\033[m')

    # Input dos dados pelo usuário
    try:
        # Validação de input do código interno único do fornecedor
        codInterno = -1
        while codInterno < 0:
            try:
                codInterno = int(input('Código do Fornecedor: '))
            except ValueError:
                print('\033[31mCódigo de tipo inválido ou nulo. Tente novamente.\033[m')
            else:
                if codInterno < 0:
                    print('\033[31mCódigo de tipo inválido. Tente novamente.\033[m')

        # Validação de input da razão social do fornecedor
        razSoc = ''
        while razSoc == '':
            razSoc = str(input('Razão Social: '))
            if razSoc == '':
                print('\033[31mDigite a razão social do fornecedor.\033[m')

        # Validação do nome fantasia do fornecedor
        nome = ''
        while nome == '':
            nome = str(input('Nome Fantasia: '))
            if nome == '':
                print('\033[31mDigite o nome fantasia do o fornecedor.\033[m')

        # Validação do CNPJ do fornecedor
        CNPJ = ''
        while not CNPJ.isnumeric():
            CNPJ = input('CNPJ (ignore os ".", "-" e "/"): ').strip()

            # Validação do formato do CNPJ (chamando a função que faz essa verificação)
            if not CNPJ.isnumeric():
                print('\033[31mFormato de CNPJ inválido. Tente novamente.\033[m')

        # O endereço do fornecedor pode ser nulo, portanto não há necessidade de validação
        endereco = str(input('Endereço: '))

        # Validação de input do telefone central do fornecedor
        telCentral = '.'
        while not telCentral.isnumeric() or len(telCentral) not in [13, 14]:
            telCentral = str(input('Telefone Central: ')).strip()

            if not telCentral.isnumeric():
                print('\033[31mFormato de telefone inválido. Tente novamente.\033[m')

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
            insert into fornecedor values (?, ?, ?, ?, ?, ?)
        """
        param = [codInterno, razSoc, nome, CNPJ, endereco, telCentral]
        cursor.execute(sql, param)
        conector.commit()
        print('\033[1;32mFornecedor registrado com sucesso.\033[m')

    except sqlite3.OperationalError:
        print('\033[31mErro ao registrar os dados.\033[m')

    # Caso uma chave primária tenha sido repetida
    except sqlite3.IntegrityError:
        print('\033[31mErro ao registrar os dados (valor de tipo único duplicado)\033[m')

    # Confirmação de loop para adicionar mais produtos
    resp = str(input('\033[1mDeseja adicionar outro fornecedor? [S/N]: \033[m')).strip().upper()[0]
    while resp not in 'SN':
        print('\033[1;33mDigite sim (S) ou não (N) para continuar.\033[m')
        resp = str(input('\033[1mDeseja adicionar outro fornecedor? [S/N]: \033[m')).strip().upper()[0]

# Fecha a conexão com o banco
cursor.close()
conector.close()

print()
print('\033[1;34mPrograma finalizado.\033[m')
