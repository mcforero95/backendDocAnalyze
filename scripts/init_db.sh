#!/bin/bash
echo "Inicializando base de datos..."
alembic revision --autogenerate -m "Inicialización de tablas"
alembic upgrade head
