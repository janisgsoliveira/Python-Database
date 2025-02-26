import sqlite3

# Conexão com o banco de dados
print('\033[1;34mConectando com o banco de dados...\033[m')
conector = sqlite3.connect("loja_pecas.db")
cursor = conector.cursor()
print('\033[1;32mConexão concluída.\033[m')

# Criação da tabela se ela não existir
try:
    sql = """
        create table clientes (
            CPF string primary key,
            nome string not null,
            RG string not null,
            endereco string,
            telFixo string,
            telCel string,
            email string
            )
        """
    cursor.execute(sql)

except sqlite3.OperationalError:
    pass

# Loop enquanto o usuário quiser adicionar um cliente
resp = 'S'
while resp == 'S':
    print('\033[1;35m-=' * 30)
    print(f'{'Informações do Cliente:':^60}')
    print('-=' * 30, '\033[m')

    # Input dos dados pelo usuário
    try:
        # Validação de input do CPF do cliente
        CPF = ''
        while not CPF.isnumeric():
            CPF = str(input('CPF (ignore os "." e o "-"): ')).strip()

            # Validação de formato do CPF
            if not CPF.isnumeric():
                print('\033[31mDigite um CPF válido.\033[m')

        # Validação de input do nome do cliente
        nome = ''
        while nome == '':
            nome = str(input('Nome: ')).strip()
            if nome == '':
                print('\033[31mDigite um nome para o cliente.\033[m')

        # Validação de input do RG do cliente
        RG = ''
        while not RG.isnumeric():
            RG = str(input('RG (ignore os "." e o "-"): ')).strip()

            # Validação de formato do RG
            if not RG.isnumeric():
                print('\033[31mDigite um RG válido.\033[m')

        # Inputs que podem ser nulos
        endereco = str(input('Endereço: ')).strip()

        # Validação do formato dos telefones
        # Telefone fixo:
        telFixo, telCel = '.', '.'
        while not telFixo.isnumeric() or len(telFixo) != 13:
            telFixo = str(input('Telefone Fixo: ')).strip()

            if telFixo == '':
                break
            elif len(telFixo) == 14:
                print('\033[31mDigite um telefone fixo neste campo.\033[m')
            else:
                if not telFixo.isnumeric() or len(telFixo) != 13:
                    print('\033[31mFormato de telefone inválido. Tente novamente.\033[m')

        # Telefone Celular:
        while not telCel.isnumeric() or len(telCel) != 14:
            telCel = str(input('Telefone Celular: ')).strip()

            if telCel == '':
                break
            elif len(telCel) == 13:
                print('\033[31mDigite um telefone celular neste campo.\033[m')
            else:
                if not telCel.isnumeric() or len(telFixo) != 14:
                    print('\033[31mFormato de telefone inválido. Tente novamente.\033[m')

        email = str(input('E-mail: ')).strip()

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
            insert into clientes values (?, ?, ?, ?, ?, ?, ?)
        """
        param = [CPF, nome, RG, endereco, telFixo, telCel, email]
        cursor.execute(sql, param)
        conector.commit()
        print('\033[1;32mCliente registrado com sucesso.\033[m')

    except sqlite3.OperationalError:
        print('\033[31mErro ao registrar os dados.\033[m')

    # Caso uma chave primária tenha sido repetida
    except sqlite3.IntegrityError:
        print('\033[31mErro ao registrar os dados (valor de tipo único duplicado)\033[m')

    # Confirmação de loop para adicionar mais produtos
    resp = str(input('\033[1mDeseja adicionar outro cliente? [S/N]: \033[m')).strip().upper()[0]
    while resp not in 'SN':
        print('\033[1;33mDigite sim (S) ou não (N) para continuar.\033[m')
        resp = str(input('\033[1mDeseja adicionar outro cliente? [S/N]: \033[m')).strip().upper()[0]

# Fecha a conexão com o banco
cursor.close()
conector.close()

print()
print('\033[1;34mPrograma finalizado.\033[m')
