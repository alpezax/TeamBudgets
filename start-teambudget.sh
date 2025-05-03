docker compose up -d 

cd teambudgets-service
uvicorn main:app --reload &
cd teambudgets-front 
streamlit run main.py &

