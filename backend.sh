#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

cd backend
fastapi dev

