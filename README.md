# Cálculo de Pontos e Combinações para Rebaixamento no Campeonato Brasileiro

Este projeto é uma aplicação em Python que permite calcular a diferença de pontos e as combinações de vitórias e empates necessárias para que um time da Série A do Campeonato Brasileiro evite o rebaixamento. A aplicação também apresenta a probabilidade de rebaixamento associada a cada time. Além disso, os dados utilizados são atualizados automaticamente a partir do processo de webscraping da página web de probabilidades da Universidade Federal de Minas Gerais: https://www.mat.ufmg.br/futebol/serie-a/.

## Funcionalidades

- **Cálculo da Diferença de Pontos:** Determina a diferença entre os pontos atuais de um time e os pontos mínimos necessários para evitar o rebaixamento.
- **Combinações de Vitórias e Empates:** Calcula e exibe todas as combinações possíveis de vitórias e empates que o time precisa para alcançar os pontos mínimos.
- **Probabilidade de Rebaixamento:** Mostra a probabilidade de rebaixamento do time selecionado.
- **Interface Gráfica:** Utiliza a biblioteca Tkinter para fornecer uma interface gráfica para o usuário.

## Dependências

Este projeto utiliza as seguintes bibliotecas:
- `requests`
- `BeautifulSoup4`
- `tkinter`
- `unicodedata`
