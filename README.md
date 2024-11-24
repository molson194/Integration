# Two-Sided Integration Test Validation

Imagine a system with a frontend service A that calls a backend service B. Traditionally, developers rely on end-to-end testing locally, end-to-end testing in production, or separate tests mocking requests/responses when initially building new contracts. This repo shows how to share mock requests and responses between the services so that developers can build each service independently. Using the mock contracts in integrations tests on the frontend and backend separately validates both services maintain forward and backward compatability. Eventually, these mocks could be used in a deployment pipeline to validate the the currently deployed dependent services succeed with the mock contracts for the new service. 

## Prereqs

* Install python
* Install node

## Scripts

* Setup: `source setup.sh`
* Backend tests: `cd backend && python -m pytest -v && cd ..`
* Playwright tests: `cd web_basic && npx playwright test && cd ..`
* Run frontend (web_basic): `python -m http.server`
* Run backend: `source .venv/bin/activate && python api.py`
* Run proxy (proxy_js): `npm start`
* Run mock_srv: `source .venv/bin/activate && python api.py -s {scenario}`
