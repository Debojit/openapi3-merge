from typing import List

from requests import Response
import requests

def derive_baseurl(url: str) -> str:
    return url.split('rest')[0] + 'rest/'

if __name__ == "__main__":
    services: List = [
        "https://gc3ossidgtl23-gc35001.integration.ocp.oraclecloud.com/ic/api/integration/v1/flows/rest/MULTIOPERATION_DEMO/1.0/metadata/openapi",
        "https://gc3ossidgtl23-gc35001.integration.ocp.oraclecloud.com/ic/api/integration/v1/flows/rest/OIC_UTIL_NOTIFICATI/1.0/metadata/openapi"
    ]

    base_url: str = derive_baseurl(services[0])
    print(base_url)
    openapi_specs: List = []

    for service in services:
        response: Response = requests.get(service)
        openapi_specs.append(response.text)
    
