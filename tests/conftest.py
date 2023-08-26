import pytest
from lever import Database
from pathlib import Path
from random import randint

DB_NAME = f'db_{randint(1, 1000)}.db'

@pytest.fixture
def db():
	DB_DIR = Path(__file__).parent.resolve() / 'databases'

	for file in DB_DIR.glob('*.db'):
		if file.name == DB_NAME:
			continue
		file.unlink()
	
	return Database(DB_DIR / DB_NAME)
