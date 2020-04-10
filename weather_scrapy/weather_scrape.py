from weather_scrapy.web_scrape import Scraper
import pickle
from translate import Translator
import time


class GrabWeather(object):
	""" The GrabWeather class contains methods and attributes created by scraping to collect weather data.

	Attributes:
		self.data (list): Containing all the scraped parts with keyword weather
		self.new_urls (list): Take only the urls from the HTML file with keyword weather
		self.location (list): Take urls for all the locations (towns - areas) in Greece
		self.translation (str): Translate the input string, of the location we want to see the weather, from English
								to greek
		self.url_needed (str): Take the final url for the location the user chose
		self.data_again (list): Reading and scraping the url_needed to get the weather data for that location
		
	"""
	def __init__(self, name):
		""" Init method to collect the name of the location the user wants to see weather data for
		
		Args:
			name (str): The name of the location

		"""

		# weather = Scraper("https://www.weather2umbrella.com/", "html.parser")
		# self.data = weather.get_spec_urls("weather")
		#
		# with open("initial data", "wb") as handle:
		# 	pickle.dump(self.data, handle)

		with open("initial data", "rb") as handle:
			self.data = pickle.load(handle)
		print(type(self.data))
		self.new_urls = []
		for url in self.data:
			if url.endswith("</a>,"):
				print(url)
				self.new_urls.append(url)

		self.location = []
		for url in self.new_urls:
			start = url.find(">")
			end = url.find("<")
			self.location.append(url[(start+1):end])

		i = 0
		for url in self.new_urls:
			start = url.find("=")
			end = url.find(">")
			self.new_urls[i] = url[(start+2): (end-1)]
			i = i + 1

		translator = Translator(to_lang="el")
		self.translation = translator.translate(name)

		index = 0
		index_needed = 0
		for names in self.location:
			if names == name:
				index_needed = index
			elif names == self.translation:
				index_needed = index
			else:
				index = index + 1

		self.url_needed = self.new_urls[index_needed]
		print(self.url_needed)

	def get_weather(self):
		""" Method to print out the weather data for the specific location. Does not return a value but only the printed
		weather data along with information about date and time.

		"""

		# weather_loc = Scraper(self.url_needed, "html.parser")
		# page_parsed = str(weather_loc.soup)
		#
		# page_parsed = page_parsed[376611:]
		#
		# with open("weather data", "wb") as handle:
		# 	pickle.dump(page_parsed, handle)

		with open("weather data", "rb") as handle:
			page_parsed = pickle.load(handle)

		self.data_again = page_parsed.split("chartData")
		needed = self.data_again[1]

		needed = needed.split("index")[1:]

		temp = []
		humidity = []
		hours = []
		winds = []
		weathers = []
		for hour in needed:

			start = hour.find("temp")
			end = hour.find("humidity")
			end_2 = hour.find("met")
			temp.append(hour[start:end])
			humidity.append(hour[end:end_2])
			hours.append(hour[:start])
			try:
				start_wind = hour.find('"windspeed":"')
				end_wind = hour.find('","fake_speed')
				wind = (hour[start_wind:end_wind])
				wind = wind.split('"')
				winds.append(wind[3])
			except:
				pass

			start_weather = hour.find("wp-content\/themes\/w2u\/image\/svg\/weather-icons-")
			end_weather = hour.find('svg","pressure"')
			weather = (hour[start_weather:end_weather])
			weather = weather.split('/')
			weather = weather[6].split('.')
			weathers.append(weather[0])

		for i in range(0, len(weathers)):
			if weathers[i] == "n01" :
				weathers[i] = "good"
			elif weathers[i] == "n02":
				weathers[i] = "quite hot"
			elif weathers[i] == "n03":
				weathers[i] = "light cloudy"
			elif weathers[i] == "n04":
				weathers[i] = "cloudy"
			elif weathers[i] == "n05":
				weathers[i] = "light rain"
			elif weathers[i] == "n08":
				weathers[i] = "extreme cloudy"
			elif weathers[i] == "n09":
				weathers[i] = "rainy"
			elif weathers[i] == "n10":
				weathers[i] = "extreme rainy"
			elif weathers[i] == "d01":
				weathers[i] = "good"
			elif weathers[i] == "d02":
				weathers[i] = "sunny"
			elif weathers[i] == "d03":
				weathers[i] = "light cloudy"
			elif weathers[i] == "d04":
				weathers[i] = "cloudy"
			elif weathers[i] == "d05":
				weathers[i] = "light rain"
			elif weathers[i] == "d08":
				weathers[i] = "extreme cloudy"
			elif weathers[i] == "d09":
				weathers[i] = "rainy"
			elif weathers[i] == "d10":
				weathers[i] = "extreme rainy"
			else:
				weathers[i] = "unexpected"

		number_temp = []
		for one in temp:
			one = one.split(":")
			new_one = one[1]
			new_one = new_one.split('"')
			number_temp.append(int(new_one[1]))

		number_hum = []
		for one in humidity:
			one = one.split(":")
			new_one = one[1]
			new_one = new_one.split('"')
			number_hum.append(int(new_one[1]))

		number_hour = []
		for one in hours:
			one = one.split(":")
			new_one = one[1]
			new_one = new_one.split('"')
			number_hour.append(int(new_one[1]))

		print("Date:", time.strftime("%d/%m/%Y"))
		j = 0
		for i in range(0, 5):
			if i % 2 == 0:
				j = j + 1
			print("At time {}.00, the weather is {}. Temperature at {} Celsius, Humidity at {}% and Wind speed at {} Beaufort"
				  .format(number_hour[i], weathers[i], number_temp[i], number_hum[i], winds[j]))


if __name__ == "__main__":

	testing = GrabWeather("Thessaloniki")
	run = testing.get_weather()






# data = pickle.dump()
# collect = Out("weather_data.txt")
# collect_pickle = Out("weather_data")
#
# collect.out_to_txt(data)
# collect_pickle.out_to_pickle(data)
