### How to run code

python3.12 -m venv venv
source venv/bin/activate
deactivate

pip install -r requirements.txt

python initialSearch.py
python filterSearch.py
python combine.py

add paper which search manually in csv table

python ris.py

python fig5.py
python fig6.py
python fig7.py

python table5.py
python table6.py

### .env

```
SEMANTIC_SCHOLAR_API_KEY=""
ELS_API_KEY=""
KEYWORDS_SEMATIC_MPA=["microplastic", "auv"]
KEYWORDS_ELSEVIER_MPA=microplastic AND auv

KEYWORDS_SEMATIC_PA=["plastic", "auv"]
KEYWORDS_ELSEVIER_PA=plastic AND auv

KEYWORDS_SEMATIC_MDM=["Microplastic","Detection","Method"]
KEYWORDS_ELSEVIER_MDM=Microplastic Detection Methods

PATHX=
```





