# Analisador de Sentimentos com spaCy e Streamlit

## Descrição
Este projeto utiliza a biblioteca **spaCy** para classificar sentimentos em frases em português com regras personalizadas e extensões do objeto `Doc`. A interface web é construída com **Streamlit** e inclui diversas funcionalidades para melhorar a experiência do usuário:

- **Customização de Dicionário**: Adicione ou remova palavras positivas e negativas dinamicamente na sidebar.
- **Logo Responsivo**: Exibe o logo no topo da sidebar, adaptando-se ao tamanho do container.
- **Análise Individual**: Selecione uma das 5 frases de exemplo ou digite sua própria frase para análise.
  - Spinner durante processamento.
  - Badge colorido com emojis (`👍`, `👎`, `😐`).
  - Expansível para exibir tokens detectados.
- **Visão Geral**: 
  - Gráfico de barras com a distribuição de sentimentos analisados.
  - Histórico de análises com opção de exportar em CSV.
- **Layout em Colunas**: Interface dividida em duas colunas para análise individual e visão geral.

## Instalação

1. Clone o repositório e entre na pasta do projeto.
2. Crie e ative o ambiente virtual:
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```
3. Atualize o pip e instale dependências:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install spacy streamlit pandas
   ```
4. Baixe o modelo de português:
   ```bash
   python -m spacy download pt_core_news_sm
   ```

## Uso

### Executar interface web
```bash
python -m streamlit run app.py
```
- A sidebar permitirá customizar o dicionário e exibirá o logo.
- Na coluna esquerda, selecione ou digite uma frase e clique em "Analisar".
- Na coluna direita, visualize o gráfico de distribuição e o histórico.
- Exporte o histórico em CSV via botão.

## Estrutura de Arquivos

```
.
├── app.py
├── logo_fiap.jpg
├── README.md
└── .venv/
```

## Integrantes
- Alan de Souza Maximiano da Silva — RM: 557088