import boto3
from bs4 import BeautifulSoup
import csv
import datetime 
import io
import json

def extract_info(html_content):
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Encontrar el archivo JSON-LD en la página
    script_tag = soup.find('script', {'type': 'application/ld+json'})
    json_data = json.loads(script_tag.string)
    results = []
    
    # Acceder a la sección "@type": "House" dentro del objeto JSON-LD
    for house in json_data['about']:
        
        
        if house['@type'] == 'House':
            neighborhood = 'Unknown'
            rooms = 0 
            bathrooms = 0
            sqm = 0
            
            print("Encontré un objeto House en la página!")
            # Hacer algo con los datos de la casa, por ejemplo:
            
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            
            try: 
                neighborhood = house['address']['addressLocality']
            except:
                print("Something went wrong")
            
            try:  
                rooms = house['numberOfBedrooms']
            except:
                print("Something went wrong")
            
            try: 
                bathrooms = house['numberOfBathroomsTotal']
            except:
                print("Something went wrong")
            
            try: 
                sqm = house['floorSize']['value']
            except:
                print("Something went wrong")
            
            results.append([date, neighborhood, rooms, bathrooms, sqm])
            
        else:
            print("No se encontró ningún objeto House en la página.")
        
    
    return results

def f(event, context):
    

    # Descargar el archivo del bucket de S3
    s3 = boto3.client("s3")
    landing_bucket = "landing-casas-123"
    final_bucket = "casas-final-0299"
    
    # Obtener el nombre del archivo
    now = datetime.datetime.now()
    key = now.strftime("%Y-%m-%d") + ".html"
    
    landing_obj = s3.get_object(Bucket=landing_bucket, Key=key)
    html_content = landing_obj["Body"].read().decode()
    
    
    results = extract_info(html_content)
    
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"
    s3.put_object(Body='', Bucket=final_bucket, Key=filename)

    with open('/tmp/{}'.format(filename), mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['FechaDescarga', 'Barrio', 'NumHabitaciones', 'NumBanos', 'mts2'])
        writer.writerows(results)

    s3.upload_file('/tmp/{}'.format(filename), final_bucket, filename)