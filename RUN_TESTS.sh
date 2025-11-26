#!/bin/bash

# Script para executar os testes do Intelecta

echo "====================================="
echo "  Executando Testes - Projeto Intelecta"
echo "====================================="
echo ""

echo "Executando testes com cobertura..."
echo ""

pytest -v --cov=. --cov-report=term-missing --cov-report=html --cov-report=xml

echo ""
echo "====================================="
echo "  Relatório de cobertura disponível em:"
echo "  htmlcov/index.html"
echo "====================================="
