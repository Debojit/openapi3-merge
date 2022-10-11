from typing import List, Dict

from requests import Response
import requests

import json

def derive_baseurl(url: str) -> str:
    return url.split("rest")[0] + "rest/"

def derive_resource_url(url: str) -> str:
    base_url: str = derive_baseurl(url)
    resource: str = "/" + url.split(base_url)[1]

    return resource

if __name__ == "__main__":
    services: List = [
        "https://gc3ossidgtl23-gc35001.integration.ocp.oraclecloud.com/ic/api/integration/v1/flows/rest/MULTIOPERATION_DEMO/1.0",
        "https://gc3ossidgtl23-gc35001.integration.ocp.oraclecloud.com/ic/api/integration/v1/flows/rest/OIC_UTIL_NOTIFICATI/1.0"
    ]

    base_url: str = derive_baseurl(services[0])

    openapi_specs: List = []
    for service in services:
        response: Response = requests.get(service + "/metadata/openapi")
        openapi_specs.append(json.loads(response.text))
    
    combined_spec: Dict = {
        "openapi": openapi_specs[0]["openapi"],
        "info": {
            "title": "Combined API Documentation",
            "version": "1.0"
        },
        "servers": [{
            "url": derive_baseurl(openapi_specs[0]["servers"][0]["url"])
        }],
        "paths": {},
        "components": {
            "schemas": {},
            "securitySchemes": {}
        }
    }

    for spec in openapi_specs:
        resource_url: str = derive_resource_url(spec["servers"][0]["url"])
        
        paths: Dict = spec["paths"]
        for path in paths.keys():
            combined_spec["paths"][resource_url + path] = paths[path]
        
        schemas: Dict = spec["components"]["schemas"]
        for schema in schemas.keys():
            combined_spec["components"]["schemas"][schema] = schemas[schema]

        security_schemes: Dict = spec["components"]["securitySchemes"]
        for scheme in security_schemes.keys():
            combined_spec["components"]["securitySchemes"][scheme] = security_schemes[scheme]

    with open('combined_spec.json', 'w') as output_file:
        output_file.write(json.dumps(combined_spec, indent=4))
