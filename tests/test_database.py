from lever import model
from tests.models import Song, Tag

def delete_all(db, model):
	items = model.get_all()
	for item in items:
		item.delete()

	db.conn.commit()

def test_database_contains_model_attributes(db):
	attrs = db.__dict__

	assert 'Model' in attrs
	assert 'Column' in attrs
	assert 'INTEGER' in attrs
	assert 'TEXT' in attrs

	assert db.Model == model.Model
	assert db.Column == model.Column
	assert db.INTEGER == model.ColumnTypes.INTEGER
	assert db.TEXT == model.ColumnTypes.TEXT

def test_database_can_create_table(db):
	db.create_table('songs', [
		db.Column('id', db.INTEGER, primary_key=True, autoincrement=True),
		db.Column('song', db.TEXT, nullable=False),
		db.Column('artist', db.TEXT, nullable=False),
		db.Column('slug', db.TEXT, nullable=False, unique=True),
		db.Column('streams', db.INTEGER, default=0),
	])

	assert 'songs' in db.tables()

def test_generate_table_name_for_model():
	tag = Tag()

	assert tag.__dict__.get('__table__') == 'tags'

def test_model_can_handle_table_args():
	song = Song(song='Breezeblocks', artist='Alt+J', slug='alt_j_breezeblocks')

	assert song.primary_key == 'id'
	assert song.fields == ['id', 'song', 'artist', 'slug', 'streams']

	assert 'id' in song.__dict__
	assert 'song' in song.__dict__
	assert 'artist' in song.__dict__
	assert 'slug' in song.__dict__

	assert song.id is None
	assert song.song == 'Breezeblocks'
	assert song.artist == 'Alt+J'
	assert song.slug == 'alt_j_breezeblocks'

def test_model_can_insert_register():
	song = Song(song='Breezeblocks', artist='Alt+J', slug='alt_j_breezeblocks')
	_id = song.save().commit()

	assert _id == 1


def test_model_can_select_fields():
	song = Song()

	res = song.select('artist, song').first()

	assert isinstance(res, Song)
	
	assert res.id
	assert res.artist == 'Alt+J'
	assert res.song == 'Breezeblocks'

def test_model_can_select_all():
	song = Song()

	res = song.first()

	assert isinstance(res, Song)
	
	res.id == 1
	res.song == 'Breezeblocks'
	res.artist == 'Alt+J'
	res.slug == 'alt_j_breezeblocks'
	res.streams == 0

def test_model_can_get_all(db):
	for i in range(100):
		song = Song(song=f'Song {i}', artist=f'Artist {i}', slug=f'slug_{i}')
		song.save()
	db.conn.commit()

	songs = Song().get_all()

	assert type(songs) == list
	assert isinstance(songs[0], Song)


def test_model_can_count():
	total = Song().count()

	assert total == 101

def test_model_can_count_with_where():
	total = Song().where('id', 90, '>').count()

	assert total == 11

def test_model_can_delete(db):
	song = Song()

	songs = Song().get_all()
	for song in songs:
		song.delete()

	db.conn.commit()

	song = Song().first()
	assert song is None

	songs = Song().get_all()
	assert len(songs) == 0

def test_model_count_returns_zero_not_none():
	total = Song().count()

	assert total == 0
	
def test_model_can_order(db):
	for i in range(1,101):
		song = Song(song=f'Song {i:03d}', artist=f'Artist {i:03d}', slug=f'slug_{i:03d}')
		song.save()
	db.conn.commit()

	songs = Song().order_by('slug DESC').get_all()

	assert songs[0].slug == 'slug_100'
	assert songs[-1].slug == 'slug_001'

	songs = Song().order_by('slug').get_all()

	assert songs[0].slug == 'slug_001'
	assert songs[-1].slug == 'slug_100'


def test_model_can_use_where(db):
	delete_all(db, Song())

	for i in range(1,101):
		song = Song(song=f'Song {i:03d}', artist=f'Artist {i:03d}', slug=f'slug_{i:03d}')
		song.save()
	db.conn.commit()

	songs = Song().where('slug', 'slug_007').get_all()
	assert len(songs) == 1

	song = Song().where('slug', 'slug_007').first()
	assert song.slug == 'slug_007'

def test_model_and_where(db):
	delete_all(db, Song())

	for i in range(1,101):
		song = Song(song=f'Song {i:03d}', artist=f'Artist {i:03d}', slug=f'slug_{i:03d}')
		song.save()
	db.conn.commit()

	songs = Song().where('slug', 'slug_007').where('artist', 'Artist 042').get_all()
	assert len(songs) == 0

	song = Song().where('slug', 'slug_007').where('artist', 'Artist 042').first()
	assert song is None

def test_model_or_where(db):
	delete_all(db, Song())

	for i in range(1,101):
		song = Song(song=f'Song {i:03d}', artist=f'Artist {i:03d}', slug=f'slug_{i:03d}')
		song.save()
	db.conn.commit()

	songs = Song().where('slug', 'slug_007').or_where('artist', 'Artist 042').get_all()
	assert len(songs) == 2
	assert songs[0].artist == 'Artist 007'
	assert songs[1].slug == 'slug_042'

def test_model_paginate_should_work_correctly(db):
	delete_all(db, Song())

	for i in range(1,1_001):
		song = Song(song=f'Song {i:03d}', artist=f'Artist {i:03d}', slug=f'slug_{i:03d}')
		song.save()
	db.conn.commit()

	res = Song().paginate()

	assert isinstance(res, model.Pagination)
	assert len(res.items) == 20
	assert isinstance(res.items[0], Song)
	assert res.page == 1
	assert res.total_items == 1_000

	res = Song().paginate(page=res.pages+1)

	assert len(res.items) == 0
