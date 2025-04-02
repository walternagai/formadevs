# Contribuindo para o FormaDevs

Primeiramente, obrigado por considerar contribuir para o FormaDevs! É graças a pessoas como você que ferramentas educacionais abertas podem evoluir e melhorar.

## Código de Conduta

Este projeto e todos os participantes estão sujeitos a um Código de Conduta. Ao participar, espera-se que você mantenha este código. Por favor, reporte comportamento inaceitável.

## Como posso contribuir?

### Reportando Bugs

Antes de criar um relatório de bug, verifique se o problema já não foi reportado procurando na seção de Issues do GitHub.

Ao criar um relatório de bug, inclua:
- Um título claro e descritivo
- Passos detalhados para reproduzir o problema
- Descrição do comportamento esperado e o que aconteceu
- Se possível, capturas de tela
- Detalhes sobre seu ambiente (SO, navegador, versão do Python e Streamlit)

### Sugerindo Melhorias

As sugestões de melhorias são rastreadas como issues do GitHub.
- Use um título claro e descritivo
- Forneça uma descrição detalhada da melhoria sugerida
- Explique por que esta melhoria seria útil para a maioria dos usuários

### Pull Requests

- Preencha o template do pull request
- Não inclua números de issues no título do PR
- Inclua capturas de tela e GIFs animados em seu PR, se aplicável
- Documente novos códigos baseando-se no estilo do projeto
- Termine todas as frases em comentários com ponto
- Evite linguagem específica de plataforma como "fechar um issue"

## Guia de Estilo

### Mensagens de Commit Git

- Use o presente imperativo: "Adiciona funcionalidade" não "Adicionada funcionalidade"
- Limite a primeira linha a 72 caracteres ou menos
- Referencie issues e pull requests livremente após a primeira linha
- Considere começar a mensagem de commit com um emoji aplicável:
    - 🎨 `:art:` quando melhorar a estrutura/formato do código
    - 🐎 `:racehorse:` quando melhorar a performance
    - 🚱 `:non-potable_water:` quando resolver memory leaks
    - 📝 `:memo:` quando escrever documentação
    - 🐛 `:bug:` quando corrigir um bug
    - 🔥 `:fire:` quando remover código ou arquivos
    - 💚 `:green_heart:` quando corrigir o CI build
    - ✅ `:white_check_mark:` quando adicionar testes
    - 🔒 `:lock:` quando lidar com segurança
    - ⬆️ `:arrow_up:` quando atualizar dependências
    - ⬇️ `:arrow_down:` quando diminuir dependências

### Python

Siga as recomendações do PEP 8 e use flake8 para verificar seu código.
- Use 4 espaços para indentação
- Limite as linhas a 79 caracteres
- Use docstrings para todas as funções, classes e métodos
- Organize as importações em grupos: padrão, terceiros, locais

### Streamlit

- Siga as diretrizes de design e UI do Streamlit
- Mantenha o código da UI separado da lógica de negócios quando possível
- Use funções para modularizar componentes da interface

## Ambiente de Desenvolvimento

### Configurando o Ambiente de Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/formadevs.git
cd formadevs

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dependências para desenvolvimento
```

### Executando Testes

```bash
# Execute todos os testes
pytest

# Execute testes com cobertura
pytest --cov=formadevs
```

## Processo de Revisão de Código

O processo de revisão de código tem como objetivo garantir a qualidade e consistência do código:

1. Outro desenvolvedor deve revisar seu código
2. O revisor irá mesclar o código após aprovar
3. O autor é responsável por resolver quaisquer problemas levantados durante a revisão

---

Novamente, obrigado por contribuir para o FormaDevs! Juntos, podemos criar uma ferramenta ainda melhor para educadores de programação.
