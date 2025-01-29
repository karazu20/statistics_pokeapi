import time

from flask import Flask, jsonify, request 

import pandas as pd
import requests
from requests.exceptions import HTTPError
import os
from typing import Optional

poke_api = os.environ.get('URL_POKE_API', "https://pokeapi.co/api/v2")


app = Flask(__name__) 


def get_data_endpoint(url: str) -> Optional[dict]:
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        return r.json()
    return r.raise_for_status()
    

def get_data_berries() -> list:

    app.logger.info(f"Getting Poke-berries...")
    berries = []
    data = get_data_endpoint(f"{poke_api}/berry")

    page_next = data.get('next', None) 
    berries = data.get('results')
    while page_next:
        data = get_data_endpoint(page_next)
        berries = berries + data.get('results')
        page_next = data.get('next', None)
    
    app.logger.info(f"Total Poke-berries: {len(berries)}")

    app.logger.info("Getting the 'growth time' for each Poke-berry...")

    for b in berries:
        data = get_data_endpoint(b.get("url"))
        b['growth_time'] = data.get('growth_time')

    return berries

def calculate_statistics(berries: list)-> dict:

    response = {}

    app.logger.info("Calculating statictics...")
    
    df = pd.DataFrame(berries)
    
    ser_growth_time = df['growth_time']

    response['berries_names'] = list(df['name'])
    response['min_growth_time'] = int(ser_growth_time.min())
    response['median_growth_time'] = round(float(ser_growth_time.median()),2)
    response['max_growth_time'] = int(ser_growth_time.max())
    response['variance_growth_time'] = round(float(ser_growth_time.var()), 2)
    response['mean_growth_time'] = round(float(ser_growth_time.mean()), 2)
    
    frecuency = dict(ser_growth_time.value_counts())
    for k, v in frecuency.items():
        frecuency[k] = int(v)
    response['frequency_growth_time'] = frecuency

    app.logger.info(f"Poke-berries statistics: {response}")

    
    return response



'''
Expected output:

Response: {

    "berries_names": [...],

    "min_growth_time": "" // time, int

    "median_growth_time": "", // time, float

    "max_growth_time": "" // time, int

    "variance_growth_time": "" // time, float

    "mean_growth_time": "", // time, float

    "frequency_growth_time": "", // time, {growth_time: frequency, ...}

}
'''


@app.route('/allBerryStats', methods=['GET']) 
def berry_statistics():
    try:
        berries = get_data_berries()
        resp = calculate_statistics(berries)
    except HTTPError:
        resp=f"Error to connect with PokeAPI {poke_api}"
        app.logger.error(resp)
        return jsonify(resp), 503
    except Exception as e:
        resp=f"Internal Error:  {e}"
        app.logger.error(resp)
        return jsonify(resp), 500

    return jsonify(resp), 200
  
  
if __name__ == '__main__': 
    app.run(debug=True)
