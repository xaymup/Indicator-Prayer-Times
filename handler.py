import ConfigParser
from prayertime import *
import os
import datetime

class Handler:
	def __init__(self):
                print "DEBUG: connecting to handler @%s" % (str(datetime.datetime.now()))
		pass
		
	def GetCalMethods(self):
		methods = ['UmmAlQuraUniv', 'EgyptianGeneralAuthorityOfSurvey', 'UnivOfIslamicSciencesKarachi', 
				'IslamicSocietyOfNorthAmerica', 'MuslimWorldLeague']
		return methods
		
	def GetMazaheb(self):
		mazaheb = ['Hanafi','Default']
		return mazaheb
		
	def GetClockFormats(self):
		clockformats = ['12h', '24h']
		return clockformats
	
	def GetOptions(self):# Gets Settings From The Configuration File
                print "DEBUG: getting settings file @%s" % (str(datetime.datetime.now()))
		options = {}
		cparse = ConfigParser.ConfigParser()
		cparse.read([os.path.expanduser('~/.indicator-prayer-times')])
		try:
			city     = cparse.get('DEFAULT', 'city')
			calcmthdname = cparse.get('DEFAULT', 'calculation-method')
			mazhabname   = cparse.get('DEFAULT', 'mazhab')
			hourfmt  = cparse.get('DEFAULT', 'clock-format')
			city_lat = float(cparse.get('DEFAULT','latitude'))
			city_lon = float(cparse.get('DEFAULT','longitude'))
			city_tz  = float(cparse.get('DEFAULT','timezone'))
                        notif = float(cparse.get('DEFAULT','notif'))
                        iconlabel = float(cparse.get('DEFAULT','iconlabel'))
			if calcmthdname == 'UmmAlQuraUniv':
				calcmthd=Calendar.UmmAlQuraUniv
			if calcmthdname == 'EgyptianGeneralAuthorityOfSurvey':
				calcmthd=Calendar.EgyptianGeneralAuthorityOfSurvey
			if calcmthdname == 'UnivOfIslamicSciencesKarachi':
				calcmthd=Calendar.UnivOfIslamicSciencesKarachi
			if calcmthdname == 'IslamicSocietyOfNorthAmerica':
				calcmthd=Calendar.IslamicSocietyOfNorthAmerica
			if calcmthdname == 'MuslimWorldLeague':
				 calcmthd=Calendar.MuslimWorldLeague

			if mazhabname == 'Default':
				 mazhab=Mazhab.Default
			if mazhabname == 'Hanafi':
				 mazhab=Mazhab.Hanafi
			options['city'] = city
			options['city_lat'] = city_lat
			options['city_lon'] = city_lon
			options['city_tz'] = city_tz
			options['cal_method_name'] = calcmthdname
			options['mazhab_name'] = mazhabname
			options['hourfmt'] = hourfmt
                        options['notif'] = notif
                        options['iconlabel'] = iconlabel
			return options
		except ConfigParser.NoOptionError:
                        print "DEBUG: No configration file using default settings"
			options['city'] = "Makkah"
			options['city_lat'] = 21.25
			options['city_lon'] = 39.49
			options['city_tz'] = 3
			options['cal_method_name'] = 'UmmAlQuraUniv'
			options['mazhab_name'] = 'Default'
			options['hourfmt'] = '24h'
                        options['notif'] = '10'
                        options['iconlabel'] = '1'
			self.SaveOptions(options)
			return options
                except ValueError:
                        print "DEBUG: Problem while reading setting file, using the default settings"
                        os.system("rm ~/.indicator-prayer-times")
                        options['city'] = "Makkah"
			options['city_lat'] = 21.25
			options['city_lon'] = 39.49
			options['city_tz'] = 3
			options['cal_method_name'] = 'UmmAlQuraUniv'
			options['mazhab_name'] = 'Default'
			options['hourfmt'] = '24h'
                        options['notif'] = '10'
                        options['iconlabel'] = '1'
			self.SaveOptions(options)
			return options

	def SaveOptions(self, options):
                print "DEBUG: saving settings file @%s" % (str(datetime.datetime.now()))
		config = open(os.path.expanduser('~/.indicator-prayer-times'), 'w')
		Text='''# Indicator-Prayer-Times Settings File
# PLEASE RESTART THE APPLICATION TO APPLY THE CHANGES

[DEFAULT]
city = %s

# Possible Values for Calculation Methods
# UmmAlQuraUniv
# EgyptianGeneralAuthorityOfSurvey
# UnivOfIslamicSciencesKarachi
# IslamicSocietyOfNorthAmerica
# MuslimWorldLeague
calculation-method = %s

# Possible Values for Mazahab
# Default
# Hanafi
mazhab = %s

# Possible Values for Clock Format
# 24h
# 12h
clock-format = %s


latitude = %s
longitude = %s
timezone = %s
notif = %s
iconlabel = %s''' % (options['city'],options['cal_method_name'], options['mazhab_name'], options['hourfmt'], options['city_lat'],
		options['city_lon'],options['city_tz'], options['notif'], options['iconlabel'])
                config.write(Text)
                config.close()

