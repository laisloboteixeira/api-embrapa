# API Embrapa – Tech Challenge

Este projeto é uma API Flask visual e funcional que realiza scraping dos dados públicos do site da Embrapa (Vitibrasil), permitindo o acesso por ano e categoria com uma interface moderna e responsiva.

## Funcionalidades

- Scraping direto do site da Embrapa por categoria e ano
- Visualização dos dados em tabela HTML
- API JSON para consumo externo
- Interface responsiva com Bootstrap 5
- Filtro por ano (1970 a 2023)
- Destaques visuais para linhas de totais e textos em caixa alta

## Estrutura

```
api_embrapa/
app.py                 # Controlador Flask (rotas e lógica)
embrapa_scraper.py     # Scraper com Pandas + BeautifulSoup
requirements.txt       # Dependências do projeto
templates/
index.html             # Página inicial com categorias
tabela.html            # Visualização da tabela com filtro
```

## Como rodar

1. Clone o repositório e acesse a pasta:
```bash
git clone https://github.com/seuusuario/api_embrapa.git
cd api_embrapa
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Rode a aplicação:
```bash
python app.py
```

4. Acesse no navegador:
```
http://localhost:5000/
```

## Endpoints

### HTML (visual)
- /producao?ano=2022
- /importacao_vinhos?ano=2023
- etc.

### API JSON
- /api/producao?ano=2022
- /api/exportacao_suco?ano=2021

## Tecnologias usadas

- Flask
- Pandas
- BeautifulSoup
- Bootstrap 5

## Sobre o scraper

O arquivo `embrapa_scraper.py` busca a URL correta com o parâmetro `ano`, encontra a melhor tabela da página, limpa os dados e formata os números. As tabelas com mais conteúdo são priorizadas.

## Observações

Este projeto foi criado para fins acadêmicos e de demonstração, e **não está licenciado para uso comercial ou distribuição pública** sem autorização.

Criado por: Laís Lobo Teixeira