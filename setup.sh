#!/bin/bash

echo "Setting Up backend"
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..
echo "Finished backend"

echo "Setting Up mock_srv"
cd mock_srv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..
echo "Finished mock_srv"

echo "Setting Up proxy_js"
cd proxy_js
npm install
cd ..
echo "Finished proxy_js"

echo "Setting Up proxy_python"
cd proxy_python
python -m venv .venv
source .venv/bin/activate
deactivate
cd ..
echo "Finished proxy_python"

echo "Setting Up web_basic"
cd web_basic
npm install
cd ..
echo "Finished web_basic"
