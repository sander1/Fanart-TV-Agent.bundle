API_KEY = '72519ab36caf49c09f69a028fb7f741d'
MOVIE_ART_URL = 'http://api.fanart.tv/webservice/movie/%s/%%s/json/moviebackground/1/2/' % (API_KEY) # IMDb or TheMovieDB id
TV_ART_URL = 'http://api.fanart.tv/webservice/series/%s/%%s/json/showbackground/1/2/' % (API_KEY) # TheTVDB id
PREVIEW_URL = '%s/preview'

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
