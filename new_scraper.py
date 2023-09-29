from bs4 import BeautifulSoup
import requests
import pandas as pd

# URL dos Exoplanetas da NASA
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Realize uma solicitação HTTP para obter o conteúdo da página
response = requests.get(START_URL)

# Verifique se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Parseie o conteúdo da página usando BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    new_planets_data = []

    def scrape_more_data(hyperlink):
        try:
            page = requests.get(hyperlink)
            soup = BeautifulSoup(page.content, "html.parser")

            temp_list = []

            for tr_tag in soup.find_all("tr", class_="fact_row"):
                td_tags = tr_tag.find_all("td")

                for td_tag in td_tags:
                    try:
                        temp_list.append(td_tag.find("div", class_="value").contents[0])
                    except:
                        temp_list.append("")

            new_planets_data.append(temp_list)

        except:
            time.sleep(1)
            scrape_more_data(hyperlink)

    planet_df_1 = pd.read_csv("updated_scraped_data.csv")

    for index, row in planet_df_1.iterrows():
        print(row['hyperlink'])
        scrape_more_data(row['hyperlink'])
        print(f"Coleta de dados do hiperlink {index+1} concluída")

    scrapped_data = []

    for row in new_planets_data:
        replaced = []
        for el in row:
            el = el.replace("\n", "")
            replaced.append(el)
        scrapped_data.append(replaced)

    headers = ["planet_type", "discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]
    new_planet_df_1 = pd.DataFrame(scrapped_data, columns=headers)
    new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")

else:
    print("Falha ao acessar a página:", response.status_code)
