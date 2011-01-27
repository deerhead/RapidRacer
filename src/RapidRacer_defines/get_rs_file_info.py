# coding: utf8

from urllib import FancyURLopener

# URL der Rapidshare API:
RS_API 					= "http://api.rapidshare.com/cgi-bin/rsapi.cgi?"
# Subroutine "Checkfile":
RS_CHECK_FILES   = "sub=checkfiles&files=" 
# Generiert File-String (für die 'checkfiles'-Routine:
RS_ADD_FILE			= lambda file_id, filename: file_id+"&"+"filenames="+filename

class RSFile():
	
	"""
	Vertritt eine Datei die auf Rapidshare liegt und enthält Informationen zu der Datei
	"""
	
	def __init__(self, url):
		
		"""
		Variablen werden erst leer gesetzt, danach anhand der lokalen Variablen
		definiert.
		"""
		
		self.__opener 	= FancyURLopener()
		self.__url		= url

		### Nun werde alle notwendigen, privaten Variablen und Listen 'deklariert'.
		### Definiert werden sie durch den Aufruf verschiedener Methoden

		self.__url_parsed	= []

		self.__filename		= ""
		self.__file_id			= ""
		self.__size				= ""
		self.__server_id		= ""
		self.__status			= ""
		self.__short_host	= ""
		self.__md5				= ""

		### Teilt die übergebene URL in ihre Bestandteile auf ###
		self.__parse_url()
		### Überprüft die Korrektheit der übergebene URL ###
		self.__check_url()

		### Setzt self.__filename und self.__file_id. Es wird davon ausgegangen,			###
		### dass das letzte und zweitletzte Element von self.__url_parsed Dateinamen###
		### und Datei-ID sind.																						###
		self.__filename  = self.__url_parsed[len(self.__url_parsed)-1]
		self.__file_id		= self.__url_parsed[len(self.__url_parsed)-2]
	
		### Holt Daten anhand der zuvor definierten URL und speichert sie in den ###
		### betreffenden Variablen																		  ###
		self.__get_info()

	def __parse_url(self):
		
		"""
		Teilt self.__url an jedem "/" und hängt es an self.__url_parsed wenn es
		länger als 0 ist.
		"""
		
		for p in self.__url.split("/"):
			if len(p):
				self.__url_parsed.append(p)
	
	def __frame_info_url(self,file_id,filename):
		
		"""
		Fügt alle bestandteile zu einer Rapidshare-API-URL zusammen
		"""
		
		return RS_API+RS_CHECK_FILES+RS_ADD_FILE(file_id,filename)
		
	def __check_url(self):

		"""
		Überprüft die korrektheit der übergebenen URL.
		"""
		if len(self.__url_parsed) < 5:
			raise SyntaxError("Scheint kein Rapidshare-Link zu sein")
		if (self.__url_parsed[1] != "rapidshare.com" and
		    self.__url_parsed[1] != "www.rapidshare.com"):
			raise SyntaxError("Scheint kein Rapidshare-Link zu sein")

	def __get_info(self):
		
		"""
		Holt die Daten aus dem Internet und übergibt sie den privaten, lokalen
		Variablen.
		"""
		
		answer = self.__opener.open(
		self.__frame_info_url(self.__file_id,self.__filename))
		
		(self.__file_id,self.__filename,self.__size,self.__server_id,
		 self.__status,self.__short_host,self.__md5) = answer.read().split(",")

	def reset_url(self, url):
		
		"""
		Ruft self.__init__ erneut auf und übergibt die neue URL
		"""
		
		self.__init__(url)

		
	def get_status(self):
		
		"""
		Gibt den Status der Datei aus.
		Zitat aus der Dokumentation der API von Rapidshare:
		
		''5:Status integer, which can have the following numeric values:
			0	= File not found
			1	= File OK (Anonymous downloading)
			3	= Server down
			4	= File marked as illegal
			5	= Anonymous file locked, because it has more than 10 downloads
				   already
			50+n = File OK (TrafficShare direct download type "n" without any logging.)
			100+n = File OK (TrafficShare direct download type "n" with logging. 
						   Read our privacy policy to see what is logged.)''
		
		Zitat Ende
		"""
		
		return self.__status