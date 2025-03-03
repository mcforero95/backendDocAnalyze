#!/bin/bash
echo "Configurando entorno..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
