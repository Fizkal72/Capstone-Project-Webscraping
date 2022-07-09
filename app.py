from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('http://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'table-responsive'})
Findrow = table.find_all('tr')

row_length = len(Findrow)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
#get Date
    period = Findrow[i].find_all('td')[0].text
    
    #get harga harian
    harga_harian = Findrow[i].find_all('td')[2].text
    harga_harian = harga_harian.strip()
       
    
    temp.append((period, harga_harian)) 

temp = temp[::-1]

#change into dataframe
exchangerates = pd.DataFrame(temp, columns = ('period','harga harian'))

#insert data wrangling here
exchangerates['harga harian'] = exchangerates['harga harian'].str.replace("IDR"," ")
exchangerates['harga harian'] = exchangerates['harga harian'].str.replace(",","")
exchangerates['harga harian'] = exchangerates['harga harian'].astype('float64')
exchangerates['period'] = exchangerates['period'].astype('datetime64')
exchangerates = exchangerates.set_index('period')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{exchangerates["harga harian"].mean()}' #be careful with the " and ' 

	# generate plot
	ax = exchangerates.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)