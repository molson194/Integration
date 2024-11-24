import pytest
from api import app
from pathlib import Path
import yaml

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

mocks_path = Path().resolve().parent / 'mocks'
files = list(Path(mocks_path).rglob('*.yaml'))
file_names = [file.stem for file in files]

@pytest.mark.parametrize('file', files, ids=file_names)
def test_scenarios(client, file):
    with file.open() as f:
        data = yaml.safe_load(f)

        for mock in data:
            endpoint = mock["route"]
            response = None
            match mock["method"]:
              case 'POST':
                response = client.post(endpoint, json=mock['body_params'])
              case 'GET':
                response = client.get(endpoint)
              case _:
                raise
            assert mock['response_body'] == response.get_json()
