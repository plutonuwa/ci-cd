#(method, endpoint, payload, expected, status_code)
temp_id = None
extract_value = None

testCase = [
    ('get','/','',{"status":"success","message": "Hello World"},None,None,None),
    ('get','/items','','',None,'extract_values',{ "item_id": ["data",0,"id"] }),
    ('get','/items','','',None,'extract_values',{"item_id":["data",0,"id"],"name":["data",0,"name"]}),
    ('get','/items/{id}','','',None,'load_query',{"id": "item_id"}),
    ]



from fastapi.testclient import TestClient
from backend.main import app
import pytest, re

client = TestClient(app)

@pytest.mark.parametrize("method,endpoint,payload,expected,status_code,extract_type,extract_path", testCase)
def test_api_endpoints(method, endpoint, payload, expected, status_code, extract_type, extract_path):

    if extract_type == 'load_query':
        endpoint = load_data(endpoint, extract_path)


    if method == "get":
        response = client.get(endpoint)
    elif method == "post":
        response = client.post(endpoint, json=payload)
    elif method == "put":
        response = client.put(endpoint, json=payload)
    # Add more methods as needed

    if status_code is not None:
        assert response.status_code == status_code
    else:
        assert response.status_code == 200

    if expected:
        assert response.json() == expected

    if extract_type == 'extract_value':
        global temp_id
        temp_id = data_extract(response.json(), extract_path)
        print(f"Extracted ID: {temp_id}")
    elif extract_type == 'extract_values':
        global extract_value
        extract_value = {key: data_extract(response.json(), path) for key, path in extract_path.items()}
        print(f"Extracted Values: {extract_value}")


def data_extract(data, path):
    try:
        for key in path:
            data = data[key]
        return data
    except KeyError:
        raise KeyError(f"Key not found in path: {path}")

def load_data(endpoint, query_params):
    print(f"Original endpoint: {endpoint}",extract_value)
    qu = re.compile(r'\{(\w+)\}')
    matches = qu.findall(endpoint)
    for param in matches:
        if param in query_params:
            print(f"Loading query parameter: {param} with value: {extract_value[query_params[param]]}")
            endpoint = endpoint.replace(f'{{{param}}}', extract_value[query_params[param]])
    return endpoint