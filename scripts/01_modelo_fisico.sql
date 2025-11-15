CREATE DATABASE IF NOT EXISTS `leilao`;

USE `leilao`;

CREATE TABLE IF NOT EXISTS `cadastros` (
        `id_usuario` int NOT NULL AUTO_INCREMENT,
        `nome` varchar(255) NOT NULL,
        `cpf` char(14) NOT NULL,
        `rg` varchar(14) NOT NULL,
        `data_nascimento` date NOT NULL,
        `email` varchar(320) NOT NULL,
        `senha` varchar(255) NOT NULL,
        `cep` char(9) NOT NULL,
        `rua` varchar(255) NOT NULL,
        `bairro` varchar(255) NOT NULL,
        `complemento` varchar(255) NOT NULL,
        `pais` varchar(255) NOT NULL,
        `cidade` varchar(255) NOT NULL,
        `estado` Enum (
            'AC',
            'AL',
            'AM',
            'AP',
            'BA',
            'CE',
            'DF',
            'ES',
            'GO',
            'MA',
            'MG',
            'MS',
            'MT',
            'PA',
            'PB',
            'PE',
            'PI',
            'PR',
            'RJ',
            'RN',
            'RO',
            'RR',
            'RS',
            'SC',
            'SE',
            'SP',
            'TO'
        ) NOT NULL,
        `telefone` VARCHAR(20) NOT NULL,
        PRIMARY KEY (`id_usuario`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_bin;

CREATE TABLE IF NOT EXISTS `adm` (
        `id_adm` int NOT NULL AUTO_INCREMENT,
        `email` varchar(320) NOT NULL,
        `senha` varchar(255) NOT NULL,
        PRIMARY KEY (`id_adm`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_bin;

CREATE TABLE IF NOT EXISTS `produtos` (
        `id_produto` int NOT NULL AUTO_INCREMENT,
        `nome_produto` varchar(255) NOT NULL,
        `descricao_produto` text,
        `categoria_produto` varchar(100),
        `preco_produto` decimal(10, 2) NOT NULL,
        `incremento_minimo` decimal(10, 2) NOT NULL,
        `id_usuario` int NOT NULL,
        PRIMARY KEY (`id_produto`),
        FOREIGN KEY (`id_usuario`) REFERENCES `cadastros` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_bin;

CREATE TABLE IF NOT EXISTS `lances` (
        `id_lance` int NOT NULL AUTO_INCREMENT,
        `valor_lance` decimal(10, 2) NOT NULL,
        `horario_lance` DATETIME DEFAULT CURRENT_TIMESTAMP,
        `id_usuario` int,
        `id_produto` int,
        PRIMARY KEY (`id_lance`),
        FOREIGN KEY (`id_usuario`) REFERENCES `cadastros` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id_produto`) ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_bin;

CREATE TABLE IF NOT EXISTS `imagens` (
        `id_imagem` int NOT NULL AUTO_INCREMENT,
        `nome_imagem` varchar(255),
        `mimetype` varchar(100),
        `img` longblob,
        `id_usuario` int,
        `id_produto` int,
        PRIMARY KEY (`id_imagem`),
        FOREIGN KEY (`id_usuario`) REFERENCES `cadastros` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id_produto`) ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_bin;