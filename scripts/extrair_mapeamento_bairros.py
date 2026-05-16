# scripts/extrair_mapeamento_bairros.py
import requests
import pandas as pd

def extrair_bairros_oficial():
    """Extrai mapeamento de bairros do GeoJSON oficial do Recife"""
    url = "https://dados.recife.pe.gov.br/dataset/area-urbana/resource/5c67ce14-1799-40c4-a37c-9daa04d1761c/download/bairros-do-recife.geojson"
    
    response = requests.get(url)
    data = response.json()
    
    bairros = []
    for feature in data['features']:
        props = feature['properties']
        bairros.append({
            'codigo_oficial': props['CBAIRRCODI'],
            'nome': props['EBAIRRNOMEOF'],
            'rpa': props['CRPAAACODI']
        })
    
    df = pd.DataFrame(bairros).sort_values('nome').reset_index(drop=True)
    df['codigo_dengue'] = df.index + 1
    
    df.to_csv('data/processed/mapeamento_bairros.csv', index=False)
    print(f"✓ {len(df)} bairros extraídos e salvos")
    
if __name__ == '__main__':
    extrair_bairros_oficial()