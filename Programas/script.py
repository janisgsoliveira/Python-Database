import sqlite3

# Conexão com o banco de dados
conector = sqlite3.connect("loja_pecas.db")
cursor = conector.cursor()

try:
    # Criação da tabela de peças
    sql = """
    create table pecas (
        codPeca integer primary key,
        descricao string,
        preco numeric not null,
        qtdeEstoque integer not null
        )
    """
    cursor.execute(sql)

    # Criação da tabela de clientes
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

    # Criação da tabela de fornecedores
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

    # Criação da tabela de contatos de fornecedores
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

    # Criação da tabela de pedidos
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

    # Criação da tabela de pedidos por item
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

cursor.close()
conector.close()
print("Programa finalizado.")
