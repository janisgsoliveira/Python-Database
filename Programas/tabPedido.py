import sqlite3

def validarData(data):
    # Validação de input vazio
    if data == '':
        return False

    # Validação de tamanho
    elif len(data) != 10:
        return False

    # Validação de caracter obirgatório
    elif data[2] and data[5] not in ['/', '-']:
        return False

    # Validação dos dígitos
    else:
        for i in range(len(data)):
            if i not in [2, 5]:
                if not data[i].isnumeric():
                    return False

    return True


# Conexão com o banco de dados
print('\033[1;34mConectando com o banco de dados...\033[m')
conector = sqlite3.connect("loja_pecas.db")
cursor = conector.cursor()
print('\033[1;32mConexão concluída.\033[m')

# Criação da tabela se ela não existir
try:
    sql = """
        create table pedido (
            numPedido integer primary key autoincrement,
            numNF integer unique not null,
            valorTotal numeric not null,
            dataPedido date not null,
            CPF string,
            foreign key(CPF) references clientes(CPF)
            )
        """
    cursor.execute(sql)

except sqlite3.OperationalError:
    pass

# Loop enquanto o usuário quiser adicionar um pedido
resp = 'S'
while resp == 'S':
    print('\033[1;35m-=' * 30)
    print(f'{'Informações do Pedido:':^60}')
    print('-=' * 30, '\033[m')

    # Input dos dados pelo usuário
    try:
        # Validação da Nota Fiscal do pedido
        NF = -1
        while NF < 0 or NF > 1000000000:
            try:
                NF = int(input('Nota Fiscal: '))
            except ValueError:
                print('\033[31mCódigo de tipo inválido ou nulo. Tente novamente.\033[m')

        # Validação do valor total do pedido
        valorTotal = 0
        while valorTotal <= 0:
            try:
                valorTotal = float(input('Valor Total: R$'))
            except ValueError:
                print('\033[31mFormato de valor inválido ou nulo. Tente novamente.\033[m')
            else:
                if valorTotal <= 0:
                    print('\033[31mFormato de valor inválido. Tente novamente.\033[m')

        # Validação da data do pedido
        data = ''
        while not validarData(data):
            data = str(input('Data do Pedido: ')).strip()

            if data == '':
                print('\033[31mDigite uma data válida.\033[m')
                print('\033[33m(ex.: 00-00-0000)\033[m')

            elif not validarData(data):
                print('\033[31mFormato de data inválido. Tente novamente.\033[m')
                print('\033[33m(ex.: 00-00-0000)\033[m')

        # Validação do CPF do cliente que efetuou o pedido
        CPF = ''
        while not CPF.isnumeric():
            CPF = str(input('CPF (ignore os "." e o "-"): ')).strip()

            # Validação de formato do CPF
            if not CPF.isnumeric():
                print('\033[31mDigite um CPF válido.\033[m')

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
            insert into pedido (numNF, valorTotal, dataPedido, cpf)
             values (?, ?, ?, ?)
        """
        param = [NF, valorTotal, data, CPF]
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
