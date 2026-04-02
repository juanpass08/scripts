# Extract Script

In this script, I’m using Playwright to query the page. It basically 'reads' the site and extracts the info since the API isn't public, but the URL is. When scraping with the library, you have to tell it when to flip the page (for example, on userfirevoice, which uses pagination). Also, you have to wait for the browser to fully load; otherwise, the query glitches out. While it’s querying and comparing results, it saves the data into a JSON and a CSV file using a specific format.

=====================================================================

En este script hago una consulta mediante "playwright", lo que hace es "Leer" la pagina y sacar la info, ya que la API no es publica peeeero la url si,
tons cuando leo con la libreria, se le tine que indicar cuando pasa de pagina (por ejemplo en userfirevoice que es por páginas) y ademas se tiene
que esperar hasta que el navegador abra por completo, sino se bugea la consulta. Mientras esta consultando y comparando resultados, los datos los
va pegando en un json y csv con un formato dado.