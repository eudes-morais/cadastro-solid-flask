CREATE TABLE Cnae (
    idCnae serial PRIMARY KEY,
    codigo varchar(7),
    descricao varchar(200)
);

CREATE TABLE Empresa (
    idEmpresa serial PRIMARY KEY,
    numeropasta int,
    razaoSocial varchar(150),
    inscricaoEstadual varchar(15),
    cnpj varchar(14) not null,
    caixaPostal varchar(10),
    email varchar(50),
    cnae_id int,
    telefone1 varchar(15),
    telefone2 varchar(15),
    FOREIGN KEY (cnae_id) REFERENCES Cnae(idCnae)
);

CREATE TABLE Funcionario (
    idFuncionario serial PRIMARY KEY,
    nomeFuncionario varchar(150),
    cpf varchar(11),
    rg varchar(11),
    orgaoExpedidor varchar(11),
    grauInstrucao varchar(25),
    nacionalidade varchar(40),
    ufnascimento integer,
    municipionascimento varchar(100),
    dataNascimento date,
    estadoCivil varchar(10),
    profissao varchar(50),
    nomePai varchar(150),
    nomeMae varchar(150),
    email varchar(50),
    cargo varchar(50),
    telefone1 varchar(15),
    telefone2 varchar(15),
    estado varchar(20),
    cidade varchar(100),
    empresafunc_id int,
    FOREIGN KEY (empresafunc_id) REFERENCES Empresa(idEmpresa)
);

CREATE TABLE OrgaoResponsavel (
    idOrgao serial PRIMARY KEY,
    nomeorgao varchar(100),
    contato varchar(50),
    telefone1 varchar(15),
    telefone2 varchar(15),
    logradouro varchar(150),
    complemento varchar(100),
    bairro varchar(100),
    cidade varchar(150),
    estado varchar(20),
    cep varchar(8)
);

CREATE TABLE EnderecoEmpresa (
    idEnderecoEmp serial PRIMARY KEY,
    logradouro varchar(150),
    complemento varchar(100),
    bairro varchar(100),
    cidade varchar(150),
    estado varchar(20),
    cep varchar(8),
    empresa_id int,
    FOREIGN KEY (empresa_id) REFERENCES Empresa(idEmpresa)
);

CREATE TABLE EnderecoFuncionario (
    idEnderecoFunc serial PRIMARY KEY,
    logradouro varchar(150),
    complemento varchar(100),
    bairro varchar(100),
    cidade varchar(150),
    estado varchar(20),
    cep varchar(8),
    funcionario_id int,
    FOREIGN KEY (funcionario_id) REFERENCES Funcionario(idFuncionario)
);

CREATE TABLE Licenca (
    idLicenca serial PRIMARY KEY,
    numeroLicenca varchar(20),
    dataInicial date,
    dataFinal date,
    valorLicenca float,
    orgao_id int,
    empresa_id int,
    produto_id integer[],
    atividade_id integer[],
    FOREIGN KEY (orgao_id) REFERENCES OrgaoResponsavel(idOrgao),
    FOREIGN KEY (empresa_id) REFERENCES Empresa(idEmpresa)
);

CREATE TABLE Produto (
    idProduto serial PRIMARY KEY,
    codProdutoNcm varchar(11),
    codNcm varchar(8),
    descricao varchar(150),
    quantidade float,
    unidadeMedida varchar(12)
);

CREATE TABLE Atividade (
    idAtividade serial PRIMARY KEY,
    descricao varchar(150)
);

CREATE TABLE Estado (
    idEstado serial PRIMARY KEY,
    codigo int,
    sigla varchar(2),
    nome varchar(20)
);

-- Garantindo TODOS os privilégios para TODAS as tabelas
GRANT ALL ON SEQUENCE public.atividade_idatividade_seq TO solid;

GRANT ALL ON SEQUENCE public.cnae_idcnae_seq TO solid;

GRANT ALL ON SEQUENCE public.empresa_idempresa_seq TO solid;

GRANT ALL ON SEQUENCE public.enderecoempresa_idenderecoemp_seq TO solid;

GRANT ALL ON SEQUENCE public.enderecofuncionario_idenderecofunc_seq TO solid;

GRANT ALL ON SEQUENCE public.funcionario_idfuncionario_seq TO solid;

GRANT ALL ON SEQUENCE public.licenca_idlicenca_seq TO solid;

GRANT ALL ON SEQUENCE public.orgaoresponsavel_idorgao_seq TO solid;

GRANT ALL ON SEQUENCE public.produto_idproduto_seq TO solid;

GRANT ALL ON SEQUENCE public.estado_idestado_seq TO solid;

GRANT ALL ON TABLE public.atividade TO solid;

GRANT ALL ON TABLE public.cnae TO solid;

GRANT ALL ON TABLE public.empresa TO solid;

GRANT ALL ON TABLE public.enderecoempresa TO solid;

GRANT ALL ON TABLE public.enderecofuncionario TO solid;

GRANT ALL ON TABLE public.funcionario TO solid;

GRANT ALL ON TABLE public.licenca TO solid;

GRANT ALL ON TABLE public.orgaoresponsavel TO solid;

GRANT ALL ON TABLE public.produto TO solid;

GRANT ALL ON TABLE public.estado TO solid;