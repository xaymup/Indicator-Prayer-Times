from gi.repository import Gtk
from handler import *
import urllib
import json
import sys
import datetime

class Configer(Gtk.Window):
	def __init__(self):
		super(Configer, self).__init__()
		self.handler = Handler()
		self.set_modal(True)
		self.set_title('Indicator prayer times preferences')
		self.set_resizable(False)
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.set_border_width(5)
		self.options = self.GetOptions()
		self.connect('destroy', self.destroy_window)
		
	def SetLayout(self):
                print "DEBUG: initializing configuration dialog @%s" % (str(datetime.datetime.now()))
		mainbox = Gtk.Box()
		mainbox.set_orientation(Gtk.Orientation.VERTICAL)
		notebook = Gtk.Notebook(border_width=5)
		##Tab 1
		tab1label = Gtk.Label('City options')
		table = Gtk.Table(border_width=5)
		table.resize(4, 2)
		#City name
		defaultcity = self.options['city']
		citylabel = Gtk.Label('Choose Your City:', xalign=0)
		self.cityentry = Gtk.Entry()
		self.cityentry.set_text('%s' % defaultcity)
		self.fetchbtn = Gtk.Button("Fetch")
		self.fetchbtn.connect('clicked', self.on_click_fetch)
		table.attach(citylabel, 0, 1, 0, 1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0 ,10)
		table.attach(self.cityentry, 1, 2, 0, 1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 10 ,10)
		table.attach(self.fetchbtn, 2, 3, 0, 1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0 ,10)
		#Latitude
		hbox1 = Gtk.Box()
		defaultlatitude = self.options['city_lat']
		latlabel = Gtk.Label('Latitude:', xalign=0)
                latadj = Gtk.Adjustment(value=0, lower=-90, upper=90, step_incr=0.01, page_incr=1, page_size=1)
		self.latentry = Gtk.SpinButton(adjustment=latadj, digits=3)
		self.latentry.set_value(float(defaultlatitude))
		table.attach(latlabel, 0, 1, 1, 2, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0 ,10)
		table.attach(self.latentry, 1, 2, 1, 2, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 10 ,10)
		#Longitude
		hbox2 = Gtk.Box()
		defaultlong = self.options['city_lon']
		longlabel = Gtk.Label("Longitude:", xalign=0)
                lngadj = Gtk.Adjustment(value=0, lower=-180, upper=180, step_incr=0.01, page_incr=1, page_size=1)
		self.longentry = Gtk.SpinButton(adjustment=lngadj, digits=3)
		self.longentry.set_value(float(defaultlong))
		table.attach(longlabel, 0, 1, 2, 3, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0 ,10)
		table.attach(self.longentry, 1, 2, 2, 3, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 10 ,10)
		tab1child = table
                #TimeZone
		hbox3 = Gtk.Box()
		defaulttz = self.options['city_tz']
                tzadj = Gtk.Adjustment(value=0, lower=-12, upper=12, step_incr=1, page_incr=1, page_size=0)
		tzlabel = Gtk.Label('Time Zone:', xalign=0)
		self.tzentry = Gtk.SpinButton(adjustment=tzadj)
		self.tzentry.set_value(float(defaulttz))
		table.attach(tzlabel, 0, 1, 3, 4, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0 ,10)
		table.attach(self.tzentry, 1, 2, 3, 4, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 10 ,10)
		##Tab2
		tab2label = Gtk.Label('Other Options')
		table = Gtk.Table(border_width=5)
		#Cal Method
		hbox3 = Gtk.Box()
		defaultmethod = self.options['cal_method_name']
		methods = self.handler.GetCalMethods()
		calmethodlabel = Gtk.Label('Calculation Method:', xalign=0)
		self.methodsmenu = Gtk.ComboBoxText(width_request=12)
		for method in methods:
			self.methodsmenu.append(method, method)
		self.methodsmenu.set_active(methods.index(defaultmethod))
		table.attach(calmethodlabel, 0, 1, 0, 1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0 ,10)
		table.attach(self.methodsmenu, 1, 2, 0, 1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 30 ,10)
		#Mazhab
		hbox4 = Gtk.Box()
		defaultmazhab = self.options['mazhab_name']
		mazhablabel = Gtk.Label('Mazhab:', xalign=0)
		mazaheb = self.handler.GetMazaheb()
		self.mazahebmenu = Gtk.ComboBoxText()
		for mazhab in mazaheb:
			self.mazahebmenu.append(mazhab, mazhab)
		self.mazahebmenu.set_active(mazaheb.index(defaultmazhab))
		table.attach(mazhablabel, 0, 1, 1, 2, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0 ,10)
		table.attach(self.mazahebmenu, 1, 2, 1, 2, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 30 ,10)
		#Clock Format
		hbox5 = Gtk.Box()
		defaultcf = self.options['hourfmt']
		clockformats = self.handler.GetClockFormats()
		cflabel = Gtk.Label('Clock Format:', xalign=0)
		self.cfmenu = Gtk.ComboBoxText()
		for cf in clockformats:
			self.cfmenu.append(cf, cf)
		self.cfmenu.set_active(clockformats.index(defaultcf))
		table.attach(cflabel, 0, 1, 2, 3, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0 ,10)
		table.attach(self.cfmenu, 1, 2, 2, 3, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 30 ,10)
		#Notification Time
                hbox6 = Gtk.Box()
                defaultvalue = self.options['notif']
                ntlabel = Gtk.Label('Time before notification:',xalign=0)
                notifadj = Gtk.Adjustment(value=0, lower=5, upper=60, step_incr=1, page_incr=1, page_size=0)
                self.ntvalue=Gtk.SpinButton(adjustment=notifadj)
                self.ntvalue.set_value(float(defaultvalue))
		table.attach(ntlabel, 0, 1, 3, 4, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0 ,10)
		table.attach(self.ntvalue, 1, 2, 3, 4, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 30 ,10)
                #Show with Icon
                hbox7 = Gtk.Box()
                showstat = self.options['iconlabel']
                silabel = Gtk.Label('Show Time left with Icon',xalign=0)
                self.sivalue=Gtk.Switch()
                if showstat==0: self.m=False
                else: self.m=True
                self.sivalue.set_active(self.m)
		table.attach(silabel, 0, 1, 4, 5, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0 ,10)
		table.attach(self.sivalue, 1, 2, 4, 5, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 30 ,10)
                tab2child = table
		#Notebook
		notebook.append_page(tab1child, tab1label)
		notebook.append_page(tab2child, tab2label)
		notebook.show_all()
		#Exit, Save Buttons
		buttons = Gtk.Box()
		spacer = Gtk.Box()
		cancel = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
		cancel.connect('clicked', self.destroy_window)
		self.okbutton = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
		self.okbutton.connect('clicked', self.on_click_ok)
		buttons.pack_start(spacer, True, True, 5)
		buttons.pack_start(cancel, False, True, 5)
		buttons.pack_start(self.okbutton, False, True, 5)
		mainbox.pack_start(notebook, True, True, 5)
		mainbox.pack_start(buttons, False, True, 5)
		mainbox.show_all()
		self.add(mainbox)
	
	def GetOptions(self):
		options = []
		options = self.handler.GetOptions()
		return options
		
	def on_click_ok(self, data):
                print "DEBUG: configuration dialog: ok button clicked @%s" % (str(datetime.datetime.now()))
		methods = self.handler.GetCalMethods()
		mazaheb = self.handler.GetMazaheb()
		clockformats = self.handler.GetClockFormats()
		####
		self.options['city'] = self.cityentry.get_text()
		self.options['cal_method_name'] = methods[self.methodsmenu.get_active()]
		self.options['mazhab_name'] = mazaheb[self.mazahebmenu.get_active()]
		self.options['hourfmt'] = clockformats[self.cfmenu.get_active()]
		self.options['city_lat'] = self.latentry.get_value()
		self.options['city_lon'] = self.longentry.get_value()
		self.options['city_tz'] = self.tzentry.get_value()
                self.options['notif'] = str(self.ntvalue.get_value())
                if self.sivalue.get_active() == True: self.b=1
                if self.sivalue.get_active() == False: self.b=0
                self.options['iconlabel'] = self.b
		print self.options
		self.handler.SaveOptions(self.options)
		self.hide()
		self.restart_app()
	
        def fetch(self, city):
		entry=self.cityentry.get_text()
                self.fetchbtn.set_label("Please wait...")
                print "DEBUG: fetching city '%s' from internet @%s" % (city, str(datetime.datetime.now()))
                try:
		        entry=self.cityentry.get_text()
                        self.fetchbtn.set_label("Please wait...")
              		url='http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % city
		        data = json.loads(urllib.urlopen(url).read())
                        return data
                except IOError:
                        print "DEBUG: Error fetching city '%s' from internet IOError: timeout @%s" % (city, str(datetime.datetime.now()))
                        self.fetchbtn.set_label("Server Error")
			self.okbutton.set_sensitive(False)
			self.fetchbtn.set_sensitive(False)
                        return None
	def on_click_fetch(self, data):
		entry=self.cityentry.get_text()
                self.fetchbtn.set_label("Please wait...")
	        self.fetchbtn.set_sensitive(False)
                data=self.fetch(entry)
                if data != None:
		    if data["status"] == "ZERO_RESULTS":
			self.fetchbtn.set_label("Invalid City")
			self.okbutton.set_sensitive(False)
		    else:
			self.okbutton.set_sensitive(True)
	           	self.fetchbtn.set_label("Fetch")
	         	self.fetchbtn.set_sensitive(True)
			self.cityentry.set_text('%s' % data["results"][0]['formatted_address'])
			self.latentry.set_value(float(data["results"][0]['geometry']['location']['lat']))
			self.longentry.set_value(float(data["results"][0]['geometry']['location']['lng']))
                        import time
                        self.tzentry.set_value(float(time.timezone / 60 / 60 * -1))

	def destroy_window(self, data):
		self.hide()
		
	def restart_app(self):
		python = sys.executable
                print "DEBUG: RESTARTING @%s" % (str(datetime.datetime.now()))
		os.execl(python, python, * sys.argv)
