import requests
import json

BASE_URL = "http://localhost:5002"
TRECHOS_FILE = "trechos_server_c.json"

def load_trechos(filename):
    with open(filename, "r") as f:
        return json.load(f)

def test_get_trechos():
    response = requests.get(f"{BASE_URL}/trechos")
    assert response.status_code == 200
    print("GET /trechos:", response.json())

def test_reserve_trecho():
    trechos = load_trechos(TRECHOS_FILE)
    if trechos:
        trecho_id = trechos[0]["id"]
        response = requests.post(f"{BASE_URL}/reserve", json={"trecho_id": trecho_id})
        assert response.status_code == 200
        print(f"POST /reserve for trecho_id {trecho_id}:", response.json())
    else:
        print("No trechos available for reservation")

def test_confirm_purchase():
    trechos = load_trechos(TRECHOS_FILE)
    if trechos:
        trecho_id = trechos[0]["id"]
        response = requests.post(f"{BASE_URL}/confirm_purchase", json={"trecho_id": trecho_id})
        assert response.status_code == 200
        print(f"POST /confirm_purchase for trecho_id {trecho_id}:", response.json())
        
        updated_trechos = load_trechos(TRECHOS_FILE)
        assert trecho_id not in [t["id"] for t in updated_trechos], "Trecho não foi removido"
        print("Trecho removido com sucesso.")
    else:
        print("No trechos available for confirmation")

if __name__ == "__main__":
    test_get_trechos()
    test_reserve_trecho()
    test_confirm_purchase()
