@echo off

pytest -vvsx --cov=.\lever --cov-report=term-missing --cov-report html
