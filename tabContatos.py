import sqlite3

# Conexão com o banco de dados
print('\033[1;34mConectando com o banco de dados...\033[m')
conector = sqlite3.connect("loja_pecas.db")
cursor = conector.cursor()
print('\033[1;32mConexão concluída.\033[m')

# Criação da tabela se ela não existir
try:
    sql = """
        create table contatos (
            idContato integer primary key autoincrement,
            codFornecedor integer,
            nome string not null,
            email string,
            telContato string not null,
            foreign key(codFornecedor) references fornecedor(codInterno)
            )
        """
    cursor.execute(sql)

except sqlite3.OperationalError:
    pass

# Loop enquanto o usuário quiser adicionar um contato de fornecedor
resp = 'S'
while resp == 'S':
    print('\033[1;35m-=' * 30)
    print(f'{'Informações do Contato de Fornecedor:':^60}')
    print('-=' * 30, '\033[m')

    # Input dos dados pelo usuário
    try:
        # Validação de input do código do fornecedor
        codForn = -1
        while codForn < 0:
            try:
                codForn = int(input('Código do Fornecedor: '))
            except ValueError:
                print('\033[31mCódigo de tipo inválido ou nulo. Tente novamente.\033[m')
            else:
                if codForn < 0:
                    print('\033[31mCódigo de tipo inválido. Tente novamente.\033[m')

        # Validação de input do nome do contato
        nome = ''
        while nome == '':
            nome = str(input('Nome: ')).strip()
            if nome == '':
                print('\033[31mDigite um nome para o contato.\033[m')

        # Input que pode ser nulo
        email = str(input('E-mail: ')).strip()

        # Validação de input do telefone do contato
        tel = ''
        while not tel.isnumeric() or len(tel) not in [13, 14]:
            tel = str(input('Telefone Fixo: ')).strip()

            if not tel.isnumeric():
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
            insert into contatos (codFornecedor, nome, email, telContato)
            values (?, ?, ?, ?)
        """
        param = [codForn, nome, email, tel]
        cursor.execute(sql, param)
        conector.commit()
        print('\033[1;32mContato registrado com sucesso.\033[m')

    except sqlite3.OperationalError:
        print('\033[31mErro ao registrar os dados.\033[m')

    # Caso uma chave primária tenha sido repetida
    except sqlite3.IntegrityError:
        print('\033[31mErro ao registrar os dados (valor de tipo único duplicado)\033[m')

    # Confirmação de loop para adicionar mais produtos
    resp = str(input('\033[1mDeseja adicionar outro contato? [S/N]: \033[m')).strip().upper()[0]
    while resp not in 'SN':
        print('\033[1;33mDigite sim (S) ou não (N) para continuar.\033[m')
        resp = str(input('\033[1mDeseja adicionar outro contato? [S/N]: \033[m')).strip().upper()[0]

# Fecha a conexão com o banco
cursor.close()
conector.close()

print()
print('\033[1;34mPrograma finalizado.\033[m')
