from lever import model

class Song(model.Model):
	__table__ = 'songs'
	primary_key = 'id'
	fields = ['id', 'song', 'artist', 'slug', 'streams']

class Tag(model.Model):
	primary_key = 'id'
	fields = ['id', 'title', 'slug']
	