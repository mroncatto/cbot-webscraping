import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json


print("Generando datos...")



try:
    # Obtiene contenido HTML a partir de URL
    url = "https://www.cmegroup.com/trading/agricultural/grain-and-oilseed/soybean.html"

    options = Options()
    options.add_argument("no-sandbox")
    options.add_argument("headless")
    options.add_argument("start-maximized")
    drive = webdriver.Chrome(chrome_options=options)
    drive.get(url)
    time.sleep(5) #Se puede aumentar el tiempo de espera si la conexión es lenta!

    #Identifica el elemento table en el DOM
    element = drive.find_element_by_xpath("//div[@class='cmeTableResponsiveScrollableWrapper']//table")
    html_content = element.get_attribute('outerHTML')

    #Parsea el contenido HTML - [BeautifulSoup]
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    #Estrutura el contenido en un Data Frame con Pandas
    #OJO: si cambia las columnas de cbotgroup hay que cambiarlas aqui tambien
    df_full = pd.read_html(str(table))[0].head(5) #puedes alterar alterar el valor dentro de 'head' para obtener mas o menos resultados
    df = df_full[['Month', 'Last', 'Change', 'Prior Settle']]
    df.columns = ['Mes', 'Ultimo', 'Alteracion', 'Liquidacion Anterior'] #Puedes cambiar los nombres de la columnas

    print(df)

    #Transforma los datos en un Diccionario de datos proprio
    first5 = {}
    first5['prices'] = df.to_dict('records')
    drive.quit()
    
    #Convierte y guarda un archivo JSON con los datos generados
    js = json.dumps(first5)
    fp = open('cbot.json', 'w')
    fp.write(js)
    fp.close()

except:
    drive.quit()
    print("Error al ejecutar el scraping!")