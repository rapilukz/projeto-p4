### Parte 1 - Scraper
Um Web scrapper a 6 sites que vai pegar 20 produtos em cada site e no fim juntar tudo num ficheiro .csv

### Sites
- [x] [Amazon](https://www.amazon.com/)
- [x] [PCDiga](https://www.pcdiga.com/)
- [x] [Nanochip](https://nanochip.pt/)
- [x] [Pc Componentes](https://www.pccomponentes.pt/)
- [x] [Chip 7](https://chip7.pt/)
- [x] [Worten](https://www.worten.pt/)

### Parte 2 - Machine Learning/Graphs
Implementação de Gráficos com base dos dados recolhidos dos csvs.


### Parte 3 - Web Application
Criação de uma web app para mostrar todos os dados recolhidos anteriormento usando flask

Para correr a app em dev:
```
py -3 -m venv .venv
python -m flask --app .\web\main.py --debug run
``` 

### Package Necessárias

```python
pip install pandas
pip install selenium
pip install seleniumbase
pip install AmazonCaptcha
pip install Flask
pip install flask_sqlalchemy
pip install seaborn
pip install matplotlib
pip install scikit-learn
```
