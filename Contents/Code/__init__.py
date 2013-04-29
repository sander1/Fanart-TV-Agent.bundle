API_KEY = '72519ab36caf49c09f69a028fb7f741d'
MOVIE_ART_URL = 'http://api.fanart.tv/webservice/movie/%s/%%s/json/moviebackground/1/2/' % (API_KEY) # IMDb or TheMovieDB id
TV_ART_URL = 'http://api.fanart.tv/webservice/series/%s/%%s/json/showbackground/1/2/' % (API_KEY) # TheTVDB id
ARTIST_ART_URL = 'http://api.fanart.tv/webservice/artist/%s/%%s/json/artistbackground/1/2/' % (API_KEY) # MusicBrainz id
ARTIST_POSTER_URL = 'http://api.fanart.tv/webservice/artist/%s/%%s/json/artistthumb/1/2/' % (API_KEY) # MusicBrainz id

PREVIEW_URL = '%s/preview'

MB_ARTIST_API = 'http://musicbrainz.org/ws/2/artist/%s'
MB_NS = {'a': 'http://musicbrainz.org/ns/mmd-2.0#'}

####################################################################################################
def Start():

	HTTP.CacheTime = CACHE_1MONTH

####################################################################################################
class FanartTVAgent(Agent.Movies):

	name = 'Fanart.tv'
	languages = [Locale.Language.NoLanguage]
	primary_provider = False
	contributes_to = [
		'com.plexapp.agents.imdb',
		'com.plexapp.agents.themoviedb'
	]

	def search(self, results, media, lang):

		if media.primary_metadata:
			results.Append(MetadataSearchResult(
				id = media.primary_metadata.id,
				score = 100
			))

	def update(self, metadata, media, lang):

		valid_names = list()
		json_obj = JSON.ObjectFromURL(MOVIE_ART_URL % metadata.id, sleep=2.0)

		if json_obj:
			key = json_obj.keys()[0]

			for img in json_obj[key]['moviebackground']:
				art_url = img['url']
				art_url_preview = PREVIEW_URL % art_url
				valid_names.append(art_url)

				if art_url not in metadata.art:
					try: metadata.art[art_url] = Proxy.Preview(HTTP.Request(art_url_preview, sleep=1.0))
					except: pass

		metadata.art.validate_keys(valid_names)

####################################################################################################
class FanartTVAgent(Agent.TV_Shows):

	name = 'Fanart.tv'
	languages = [Locale.Language.NoLanguage]
	primary_provider = False
	contributes_to = [
		'com.plexapp.agents.thetvdb'
	]

	def search(self, results, media, lang):

		if media.primary_metadata:
			results.Append(MetadataSearchResult(
				id = media.primary_metadata.id,
				score = 100
			))

	def update(self, metadata, media, lang):

		valid_names = list()
		json_obj = JSON.ObjectFromURL(TV_ART_URL % metadata.id, sleep=2.0)

		if json_obj:
			key = json_obj.keys()[0]

			for img in json_obj[key]['showbackground']:
				art_url = img['url']
				art_url_preview = PREVIEW_URL % art_url
				valid_names.append(art_url)

				if art_url not in metadata.art:
					try: metadata.art[art_url] = Proxy.Preview(HTTP.Request(art_url_preview, sleep=1.0))
					except: pass

		metadata.art.validate_keys(valid_names)

####################################################################################################
class FanartTVAgent(Agent.Artist):

	name = 'Fanart.tv'
	languages = [Locale.Language.NoLanguage]
	primary_provider = False
	contributes_to = [
		'com.plexapp.agents.lastfm'
	]

	def search(self, results, media, lang):

		# Get the MusicBrainz id from the Last.fm Agent
		mb_id = Core.messaging.call_external_function(
			'com.plexapp.agents.lastfm',
			'MessageKit:GetMbIdForArtist',
			kwargs = dict(
				artist = media.primary_metadata.title
			)
		)

		if mb_id:
			results.Append(MetadataSearchResult(
				id = mb_id,
				score = 100
			))

	def update(self, metadata, media, lang):

		# Artist art
		valid_names = list()
		json_obj = JSON.ObjectFromURL(ARTIST_ART_URL % metadata.id, sleep=2.0)

		if not json_obj:
			try:
				mb_id = XML.ElementFromURL(MB_ARTIST_API % metadata.id).xpath('//a:artist/@id', namespaces=MB_NS)[0]
				json_obj = JSON.ObjectFromURL(ARTIST_ART_URL % mb_id, sleep=2.0)
			except:
				json_obj = None

		if json_obj:
			key = json_obj.keys()[0]

			for img in json_obj[key]['artistbackground']:
				art_url = img['url']
				art_url_preview = PREVIEW_URL % art_url
				valid_names.append(art_url)

				if art_url not in metadata.art:
					try: metadata.art[art_url] = Proxy.Preview(HTTP.Request(art_url_preview, sleep=1.0))
					except: pass

		metadata.art.validate_keys(valid_names)

		# Artist posters
		valid_names = list()
		json_obj = JSON.ObjectFromURL(ARTIST_POSTER_URL % metadata.id, sleep=2.0)

		if not json_obj:
			try:
				mb_id = XML.ElementFromURL(MB_ARTIST_API % metadata.id).xpath('//a:artist/@id', namespaces=MB_NS)[0]
				json_obj = JSON.ObjectFromURL(ARTIST_POSTER_URL % mb_id, sleep=2.0)
			except:
				json_obj = None

		if json_obj:
			key = json_obj.keys()[0]

			for img in json_obj[key]['artistthumb']:
				poster_url = img['url']
				poster_url_preview = PREVIEW_URL % poster_url
				valid_names.append(poster_url)

				if poster_url not in metadata.posters:
					try: metadata.posters[poster_url] = Proxy.Preview(HTTP.Request(poster_url_preview, sleep=1.0))
					except: pass

		metadata.posters.validate_keys(valid_names)
