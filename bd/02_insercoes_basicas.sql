INSERT INTO adm (email, senha) 
VALUES
    ("fabii@gmail.com", "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"),
    ("biaa@gmail.com", "fe2592b42a727e977f055947385b709cc82b16b9a87f88c6abf3900d65d0cdc3");

INSERT INTO cadastros (nome, cpf, data_nascimento, email, senha, cep, rg, rua, bairro, complemento, pais, cidade, telefone, estado) 
VALUES 
    (
        'Fabi', '445.678.678-98', '2009-09-09', 'fabis@gmail.com', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 
        '12345678', '45.678.123-0', 'Rua das Flores', 'Centro', 'Casa 2', 
        'Brasil', 'São Paulo', '11987654321', 'SP'
    ),
    (
        'Maria', '998.776.675-86', '1980-09-07', 'mria@hormail.com', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 
        '98798798', '33.456.987-4', 'Av. Brasil', 'Jardins', 'Apto 101', 
        'Brasil', 'Rio de Janeiro', '21999887766', 'RJ'
    ),
    (
        'Julio', '098.665.445-87', '2009-12-16', 'hulio@gmail.com', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 
        '12312312', '12.345.678-9', 'Rua Azul', 'Vila Nova', 'Fundos', 
        'Brasil', 'Curitiba', '41988776655', 'PR'
    ),
    (
        'nana', '845.678.678-58', '2010-05-30', 'nana@gmail.com', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 
        '23443223', '98.765.123-1', 'Rua Bela Vista', 'Centro', 'Bloco B', 
        'Brasil', 'Salvador', '71987654321', 'BA'
    );

INSERT INTO produtos (nome_produto, categoria_produto, data_final, preco_produto, incremento_minimo, descricao_produto, id_usuario) 
VALUES 
    ('caneca', 'casual', '2009-09-09', 20.99, 5.00,'descricao muitolongaaaaaaaaaaaaaa', 2),
    ('flor', 'casual','2008-08-08', 45.99, 10.00, 'descricao mais longa aindaaaaaaaa',3);

INSERT INTO lances (valor_lance, horario_lance, id_usuario, id_produto) 
VALUES 
    (21.99, '2025-10-26 14:30:00', 2, 1),
    (46.99, '2025-10-27 14:30:00', 3, 2);