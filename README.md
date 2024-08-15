# Sistema de Gerenciamento de Registros com Google Sheets

## Descrição

Este projeto é uma aplicação web desenvolvida com Flask, que utiliza a API do Google Sheets para gerenciamento e manipulação de dados. A aplicação permite adicionar, editar, excluir e pesquisar registros armazenados em uma planilha do Google Sheets, proporcionando uma interface web intuitiva para o gerenciamento de dados.

## Funcionalidades

- **Visualização de Registros**: Exibe uma tabela com todos os registros da planilha do Google Sheets e fornece um formulário para adicionar ou editar registros.
- **Adição e Edição de Registros**: Permite adicionar novos registros e editar registros existentes com base no `ID`.
- **Exclusão de Registros**: Remove registros específicos com base no `ID` fornecido.
- **Pesquisa de Registros**: Filtra registros por `ID`, `Nome`, `Empresa` e `Localização`.
- **Gerenciamento de Erros**: Mensagens de erro e sucesso são exibidas para informar o usuário sobre o status das operações.

## Tecnologias Utilizadas

- **Flask**: Framework web leve em Python para construção da aplicação.
- **Google Sheets API**: Interface para interação com planilhas do Google Sheets.
- **python-dotenv**: Biblioteca para carregar variáveis de ambiente a partir de um arquivo `.env`.

## Configuração

### Requisitos

- Python 3.x
- Pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório:**

   ```sh
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio
