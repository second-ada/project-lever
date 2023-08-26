from lever import migration


def test_db_have_migration_attribute(db):
	assert db.Migration == migration.Migration


def test_db_migration_can_drop_tables(db):
	db.drop_table('songs')

	assert 'songs' not in db.tables()
