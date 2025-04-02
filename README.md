# FormaDevs

## Sobre o Projeto

FormaDevs é uma aplicação Streamlit que facilita a formação de grupos de estudantes para projetos, laboratórios e atividades em turmas de programação. Projetada para professores e instrutores que precisam organizar rapidamente seus alunos em equipes de trabalho, a aplicação oferece diversas opções de formação de grupos e gerenciamento de informações.

## 🚀 Funcionalidades

- **Múltiplos métodos de formação de grupos**:
  - Aleatório: distribuição completamente randômica
  - Sequencial: grupos formados na ordem da lista
  - Balanceado: distribuição que tenta equilibrar os grupos

- **Interface intuitiva e completa**:
  - Menu de navegação lateral
  - Temas personalizáveis
  - Visualização detalhada dos grupos

- **Entrada flexível de dados**:
  - Entrada manual (formato "Matrícula, Nome")
  - Importação via CSV
  - Carregamento de dados salvos anteriormente

- **Exportação versátil**:
  - CSV
  - Excel
  - Listas por grupo

- **Gestão de histórico**:
  - Salva grupos formados anteriormente
  - Permite reutilização de conjuntos de alunos
  - Rastreabilidade das formações de grupos

- **Configurações personalizáveis**:
  - Tamanho padrão dos grupos
  - Método de formação
  - Opções de redistribuição de alunos

## 📋 Pré-requisitos

- Python 3.7+
- Streamlit
- Pandas
- Outras dependências (listadas em `requirements.txt`)

## 🔧 Instalação

1. Clone o repositório:
```
git clone https://github.com/seu-usuario/formadevs.git
cd formadevs
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

3. Execute a aplicação:
```
streamlit run app.py
```

## 📖 Como Usar

### Entrada de Dados
1. Acesse a aba "Formar Grupos"
2. Insira os dados dos estudantes em uma das seguintes formas:
   - Digite manualmente no formato "Matrícula, Nome"
   - Importe um arquivo CSV
   - Carregue de um conjunto salvo anteriormente

### Configuração dos Grupos
1. Defina o tamanho desejado para os grupos (entre 2 e 8 estudantes)
2. Escolha o método de formação (Aleatório, Sequencial ou Balanceado)
3. Ajuste as opções avançadas, se necessário:
   - Redistribuir estudantes sozinhos
   - Permitir grupos maiores que o limite
   - Definir uma semente aleatória para reproduzir resultados

### Visualização e Exportação
1. Após formar os grupos, navegue pelas abas para ver cada grupo
2. Use a aba "Visão Geral" para ver estatísticas e a distribuição completa
3. Exporte os resultados no formato desejado (CSV, Excel)

## 🎯 Casos de Uso

- **Projetos em Equipe**: Forme grupos balanceados para projetos de programação
- **Laboratórios de Prática**: Crie pares ou pequenos grupos para atividades práticas
- **Hackathons**: Distribua alunos em equipes de forma rápida e justa
- **Monitorias**: Organize grupos de estudo ou grupos de tutoria entre pares

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma Branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

Consulte também o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.

## 📬 Contato

Walter A. Nagai - [walternagai@unifei.edu.br](mailto:walternagai@unifei.edu.br)

Link do projeto: [https://github.com/walternagai/formadevs](https://github.com/walternagai/formadevs)

---

⭐️ Desenvolvido com ❤️ para a comunidade educacional de programação ⭐️
