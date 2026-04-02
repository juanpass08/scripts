import json
import csv
import time
from playwright.sync_api import sync_playwright

# En este script hago una consulta mediante "playwright", lo que hace es "Leer" la pagina y sacar la info, ya que la API no es publica peeeero la url si,
# tons cuando leo con la libreria, se le tine que indicar cuando pasa de pagina (por ejemplo en userfirevoice que es por páginas) y ademas se tiene
# que esperar hasta que el navegador abra por completo, sino se bugea la consulta. Mientras esta consultando y comparando resultados, los datos los
# va pegando en un json y csv con un formato dado.

def main():
    url = "https://firebase.uservoice.com/forums/948424-general"
    all_data = [] 
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # -> Se supone que con esto, no se necesita abrir un navegador.Cambiar a False si se quiere ver como el browser funciona con estas funciones.
        page = browser.new_page() #Litreal abres una pestaña
        page.goto(url)#La pestaña es la url que queremos ver, ósea Firebase UserVoice.

        print("Cargando más sugerencias...") #Esto de acá simula lo que se haría con el mouse. Hacer un scroll, click en los resultados y pasar de página.
        for _ in range(3):
            page.mouse.wheel(0, 5000) # acá se mueve el mouse por la pantalla y los 5000 son los píxeles.
            time.sleep(2)# un sleep de toda la vida, permites que "respire" para poder hacer otra petición.

        #Aquí se comienza la captura de info. 
        items = page.query_selector_all(".uvIdeaTitle a")#Aquí le dices a Playwright: "Busca todos los elementos que sean etiquetas <a> (enlaces) que estén dentro de algo llamado .uvIdeaTitle".
        links = [ "https://firebase.uservoice.com" + i.get_attribute("href") for i in items ] #Esta línea recorre cada item encontrado, extrae la parte final del enlace (href) y le pega el dominio de Firebase al principio para que tengas la URL completa y funcional.

        print(f"Se encontraron {len(links)} propuestas. Extrayendo descripciones...")

        for link in links[:50]: #Para test, solo procese las primeras 50.
                page.goto(link) # Aqui el browser va a navegar tal cual a la página.
                page.wait_for_selector(".uvIdeaDescription") #Aquí practicamente es: No intentes leer nada hasta que la descripción aparezca en pantalla
                
                title = page.inner_text(".uvIdeaTitle")#El inner text extrae el puro texto, sin nada de html.
                description = page.inner_text(".uvIdeaDescription") 
                
                all_data.append({ #Acá se guarda todo lo que nos truje chencha. solo contruyes el objeto, no guardas.
                    "title": title.strip(),
                    "description": description.strip(),
                    "url": link,
                    "extracted_at": "2026-03-23"
                })

        browser.close() #se cierra el browser. ya acabó

    with open('fr_data_uservoice.json', 'w', encoding='utf-8') as f: #Le damos el nombre y formato al archivo donde metemos la data. Cosa interesante con el with cierra el archivo aunqe haya un error.
        json.dump(all_data, f, indent=4, ensure_ascii=False)#Esto de aqui no se muy bien como funciona pero toma la lista All data y la hace json.

    headers = ["title", "description", "url", "extracted_at"]
    
    with open('fr_data_uservoice.csv', 'w', newline='', encoding='utf-8') as f: #Tambien no se muy bien como funciona todo al 100 pero acá sacas en .csv
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=',')
        writer.writeheader()
        writer.writerows(all_data)
        
    print(f"Archivo CSV generado con éxito con {len(all_data)} filas.")

main()