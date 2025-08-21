.PHONY: data preprocess eda sql geo train eval dashboard test clean

data:
	python src/fetch_api.py
	python src/scrape_wiki.py
	python src/wrangle.py

preprocess:
	python src/wrangle.py

eda:
	@echo "Open notebooks/03_eda_sql.ipynb in Jupyter"

sql:
	@echo "Run SQL queries from sql/queries.sql against data/processed/spacex.db"

geo:
	python src/visualize.py --make-map

train:
	python src/train.py

eval:
	python src/eval.py

dashboard:
	python app/dashboard.py

test:
	pytest -q

clean:
	rm -rf data/interim/* data/processed/* models/* logs/* || true