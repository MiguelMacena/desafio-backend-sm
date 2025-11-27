API desenvolvida como desafio técnico para vaga de **Backend Júnior**, utilizando:

- Django + Django REST Framework  
- Integração com a PokeAPI  
- Redis como cache  
- Testes com Pytest  
- GitHub Actions (CI)  - black, flake8 e isort

O projeto permite gerenciar treinadores, pokémons, associações e batalhas.

---

## 🚀 Tecnologias

- Python 3.11
- Django 4+
- DRF
- Redis (cache)
- Pytest
- GitHub Actions (CI)

---

🧠 Cache (Redis)
Cacheados:

Resposta da PokeAPI (TTL 10 min)
Lista de treinadores;
Lista de pokémons;
Pokémons de um treinador;

Invalidação automática:
CRUD de treinador
CRUD de pokémon
add/remove de pokémon do treinador

---

🧪 Testes

Rodar testes:

pytest -q

Cobertura inclui:
Models;
Serializers;
Views;
Fluxo completo de batalha (integração);
Testes do Redis (cache + invalidação);

---

# 🔧 Instalação e Execução

## 1️⃣ Clone o repositório

git clone https://github.com/MiguelMacena/desafio-backend-sm.git

## 2️⃣ Crie e ative um ambiente virtual
Windows:
python -m venv venv
venv\Scripts\activate

Linux:
python3 -m venv venv
source venv/bin/activate

##3️⃣ Instale as dependências

pip install -r requirements.txt

##4️⃣ Inicie o Redis localmente

Linux:
sudo apt install redis-server
sudo systemctl start redis

Windows:
instalar via WSL 

##5️⃣ Execute as migrações

python manage.py migrate


##6️⃣ Suba o servidor

python manage.py runserver

-----------------------------------------------

📡 Endpoints
-----------------------------------------------
Base URL:

http://localhost:8000/api/v1/

👤 Treinadores
GET  -  /trainers/ <br>
POST - /trainers/ <br>
GET  -  /trainers/id/ <br>
PUT  -  /trainers/id/ <br>
DELETE - /trainers/id/ <br>


🔥 Pokémons
GET  - /pokemons/ <br>
POST - /pokemons/  → cria e busca dados na PokeAPI <br>
GET  -  /pokemons/id/ <br>
DELETE - /pokemons/id/ <br>


🧩 Associar Pokémon a Treinador
POST - /trainers/trainer.id/add-pokemon/
GET - /trainer-pokemons/

🗑️ Remover Pokémon do Treinador
DELETE - /api/v1/trainers/trainer.id/remove-pokemon/pokemon.id/

🥊 Batalha Pokémon
POST - /api/v1/battle/
