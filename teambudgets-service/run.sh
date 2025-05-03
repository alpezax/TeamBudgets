while true; do
    uvicorn main:app --reload
    echo "El proceso uvicorn se ha detenido. Reiniciando..."
    sleep 1
done