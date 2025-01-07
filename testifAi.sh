#exec > /tmp/fastapi.log 2>&1

#env

# You may need to add here things like : source .../.bashrc

echo "Starting FastAPI..."
$HOME/miniconda3/bin/uvicorn server:app --host 0.0.0.0 --port 8000
