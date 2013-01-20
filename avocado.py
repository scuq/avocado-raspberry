#!/usr/bin/python
# coding=utf-8
# -*- coding: <utf-8> -*-
# vim: set fileencoding=<utf-8> :

# Copyright (C) 2013    Stefan Nistelberger (scuq at abyle.org)
#
# avocado 
# avocado - geek kiosk script for rasbian
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# http://www.gnu.org/licenses/gpl.txt
#
# dependencies: midori dillo omxplayer cclive qiv
# recommends: lighttpd samba php5-cgi
#
# avocado creates a queue of avocado-items (youtube, webbrowse, local picture show)
#
# youtube vids are downloaded with cclive and played with omxplayer
# you need enough diskspace because the vids are cached in the avocado cache dir
#
# webbrowse launches midori and display the page for the given time (timeout) default is 30 minutes
# 
# local pictures are displayed with qiv, all pictures have to be in one directory (can be filled with samba)
#
# if you enable the --kiosk(mode) avocado keeps playing and displaying the previous items randomly 
# till you add new ones or the pi is burning
#
# for your convenience the avocado queue can be viewed and filled by a simple webinterface running on lighttpd with php5-cgi 
#
# todos:
# - cache disk space check
# - random kiosk queue
# - qiv
#
# version: 0.1 - early dirty alpha hack
# changelog:
# 
# 
# 

scriptid="avocado"

import sys
import stat
import re
import os
import base64
import time
import glob
import httplib, urllib
import logging
from shutil import copy
from logging.handlers import SysLogHandler
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(scriptid)
logger.setLevel(logging.INFO)
syslog = SysLogHandler(address='/dev/log',facility="local4")
formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
syslog.setFormatter(formatter)
logger.addHandler(syslog)
from optparse import OptionParser
from pwd import getpwnam
import tempfile
from subprocess import Popen, PIPE, STDOUT

# daemon filehandles
import resource

def human_size(size_bytes):
    """
    format a size in bytes into a 'human' file size, e.g. bytes, KB, MB, GB, TB, PB
    Note that bytes/KB will be reported in whole numbers but MB and above will have greater precision
    e.g. 1 byte, 43 bytes, 443 KB, 4.3 MB, 4.43 GB, etc
    """
    if size_bytes == 1:
        # because I really hate unnecessary plurals
        return "1 byte"

    suffixes_table = [('bytes',0),('KB',0),('MB',1),('GB',2),('TB',2), ('PB',2)]

    num = float(size_bytes)
    for suffix, precision in suffixes_table:
        if num < 1024.0:
            break
        num /= 1024.0

    if precision == 0:
        formatted_size = "%d" % num
    else:
        formatted_size = str(round(num, ndigits=precision))

    return "%s %s" % (formatted_size, suffix)

def realDaemon(avocadoDir, avocadoWebDir, avocadoQueueDir, avocadoCacheDir, avocadoCacheValidateDir, avocadoKioskQueueDir, kioskmode=False):

        # first fork
    try:
        pid = os.fork()
        if pid > 0:
        # exit first parent
            sys.exit(0)
    except (OSError):
        print (str(sys.exc_info()[1]))
        sys.exit(1)

    # change environment
    os.chdir("/")

    # session leader of this new session and process group leader of the new process group
    os.setsid()
    os.umask(0)

    # second fork, causes the second child process to be orphaned making the init process responsible for its cleanup

    try:
        pid = os.fork()
        if pid > 0:
        # exit from second parent, print eventual PID before
        #print "Daemon PID %d" % pid
        #open(PIDFILE,'w').write("%d"%pid)
            sys.exit(0)
    except (OSError):
        print (str(sys.exc_info()[1]))
        sys.exit(1)



    # retrieve the maximum file descriptor number if there is no limit on the resource, use the default value
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if (maxfd == resource.RLIM_INFINITY):
        maxfd = "1024"

    # close all file descriptors
    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError: # ERROR, fd wasn't open to begin with (ignored)
            pass

    # # standard input (0)
    os.open("/dev/null", os.O_RDWR)

    # duplicate standard input to standard output and standard error.
    os.dup2(0, 1)
    os.dup2(0, 2)

    # daemon code
    avocadoDaemon(avocadoDir, avocadoWebDir, avocadoQueueDir, avocadoCacheDir, avocadoCacheValidateDir, avocadoKioskQueueDir, kioskmode)

def avocadoDaemon(avocadoDir, avocadoWebDir, avocadoQueueDir, avocadoCacheDir, avocadoCacheValidateDir, avocadoKioskQueueDir, kioskmode=False):

	logger.info("avocadoDaemon started.")


	try:
		while True:
			time.sleep(2)
			logger.info("avocadoDaemon run nextInQ")
			nextInQ(avocadoQueueDir,avocadoCacheDir,avocadoCacheValidateDir,avocadoDir,avocadoWebDir, avocadoKioskQueueDir, kioskmode)
	except:
		logger.error("avocadoDaemon exited unexpectedly")


def unsetWebStatus(avocadoDir):

        try:
                f = open(avocadoDir+"status.txt", "w")
                try:
                        f.write("unkown")
                finally:
                        f.close()
        except IOError:
                pass


	p = Popen("killall dillo", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

def setWebStatus(avocadoDir, text):

	try:
		f = open(avocadoDir+"status.txt", "w")
		try:
			f.write(text.encode('utf-8'))
		finally:
			f.close()
	except IOError:
		pass

	_command="export DISPLAY=:0.0 && dillo -f -g 1920x1080 http://localhost/status.php &"
	logger.info(_command)
	p = Popen(_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

	return

	


def retrim(inputstr):

	inputstr = re.sub("^[^\w]+","",inputstr)
	inputstr = re.sub("[^\w]+$","",inputstr)
	inputstr = re.sub(" +"," ",inputstr)

	return inputstr



def addToQ(avocadoQueueDir, avocadoKioskQueueDir, item, type, timeout):

	temp = tempfile.NamedTemporaryFile(prefix=avocadoQueueDir,delete=False)
	temp.write(type+"\n")
	temp.write(item+"\n")
	temp.write(timeout+"\n")
	temp.close()
	os.chmod(temp.name, 0664)

	copy(temp.name, avocadoKioskQueueDir+os.path.basename(temp.name))
	print avocadoKioskQueueDir+os.path.basename(temp.name)
	os.chmod(avocadoKioskQueueDir+os.path.basename(temp.name), 0664)




def removeFromQ(avocadoQueueDir, item):

	if os.path.isfile(avocadoQueueDir+item):
		os.unlink(avocadoQueueDir+item)
		logger.info("queue item removed: "+avocadoQueueDir+item)



def getCContents(avocadoCacheDir):

	c={}
	csize=0

        _c = [s for s in os.listdir(avocadoCacheDir)

        if os.path.isfile(os.path.join(avocadoCacheDir, s))]

        _c.sort(key=lambda s: os.path.getmtime(os.path.join(avocadoCacheDir, s)))

	for _itemname in _c:
		try:
			_item=""
			_item=base64.b64decode(_itemname)

			csize=csize+os.path.getsize(avocadoCacheDir+_itemname)
			
			ci={}
			ci["item"]=_item
       		        ci["mtime"]=os.path.getmtime(avocadoCacheDir+_itemname)
       		        ci["size"]=human_size(os.path.getsize(avocadoCacheDir+_itemname))
       		        ci["type"]="cache"
			c[_itemname]=ci
		except:
			pass

	csize=human_size(csize)

	return c, csize
			


def getQContents(avocadoQueueDir):

        q={}

        _q = [s for s in os.listdir(avocadoQueueDir)

        if os.path.isfile(os.path.join(avocadoQueueDir, s))]

        _q.sort(key=lambda s: os.path.getmtime(os.path.join(avocadoQueueDir, s)))


        for _itemname in _q:
		try:
                	_item=""
               		_type=""
                	_fh = open (avocadoQueueDir+_itemname,"r")
			_lines = _fh.readlines()
                	_type = retrim(_lines[0])
                	_item = retrim(_lines[1])
                	_timeout = retrim(_lines[2])
                	_fh.close()

        		qi={}
	                qi["item"]=_item
       		        qi["type"]=_type
       		        qi["timeout"]=_timeout
       		        qi["mtime"]=os.path.getmtime(avocadoQueueDir+_itemname)
			q[_itemname]=qi

		except Exception, e:
			os.unlink(avocadoQueueDir+_itemname)
			logger.warning("removed invalid queue-file: "+avocadoQueueDir+_itemname+" "+e.message)
			pass


	return q

def nextInQ(avocadoQueueDir,avocadoCacheDir,avocadoCacheValidateDir,avocadoDir,avocadoWebDir, avocadoKioskQueueDir, kioskmode=False):
	
	contents = getQContents(avocadoQueueDir)

	try:
		job = contents[contents.keys()[0]]
	except IndexError:
		if kioskmode:
			contents = getQContents(avocadoKioskQueueDir)
		else:
			return

        try:
                job = contents[contents.keys()[0]]
		logger.info("nothin in queue, usig kiosk queue")
        except IndexError:
		logger.info("avocado kiosk queue is empty")
		return

	jobname = contents.keys()[0]

	logger.info("next Q item: "+jobname+" "+str(job))

	if job["type"]=="youtube":

		# check if a think that there is a valid cached file
		if not os.path.exists(avocadoCacheValidateDir+base64.b64encode(job["item"])):

			if os.path.exists(avocadoCacheDir+base64.b64encode(job["item"])):
				logger.warn("removing invalid cached file: "+avocadoCacheDir+base64.b64encode(job["item"]))
				os.unlink(avocadoCacheDir+base64.b64encode(job["item"]))

			_command="cclive -n "+job["item"]
			logger.info(_command)
			p = Popen(_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
			_statustext="DOWNLOADING ...<BR>"
			for line in p.stderr.readlines():
				if line.count("WARNING") == 0:
					_statustext += line.decode("utf-8")
					_statustext += "<br>"

			
			setWebStatus(avocadoDir,_statustext)

			
			_command="cclive --format=fmt22_720p --output-file="+avocadoCacheDir+base64.b64encode(job["item"])+" "+job["item"]
			logger.info(_command)
			p = Popen(_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
			logger.info(re.sub('\\n+','',str(p.stdout.read().decode("utf-8"))))
			logger.error(re.sub('\\n+','',str(p.stderr.read().decode("utf-8"))))


			if os.path.isfile(avocadoCacheDir+base64.b64encode(job["item"])):
				logger.info("creating cache valid  file: "+avocadoCacheValidateDir+base64.b64encode(job["item"]))
				open(avocadoCacheValidateDir+base64.b64encode(job["item"]), 'w').close() 

		_command="export DISPLAY=:0.0 && omxplayer "+avocadoCacheDir+base64.b64encode(job["item"])

		logger.info(_command)
		setWebStatus(avocadoDir,_command)

		p = Popen(_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
		logger.info(re.sub('\\n+','',str(p.stdout.read().decode("utf-8"))))
		logger.error(re.sub('\\n+','',str(p.stderr.read().decode("utf-8"))))

		unsetWebStatus(avocadoDir)
		removeFromQ(avocadoQueueDir, jobname)

	if job["type"]=="webbrowse":

		_command="export DISPLAY=:0.0 && timeout "+job["timeout"]+" midori -e Fullscreen -a "+job["item"]+" 2>/dev/null"
		#_command="export DISPLAY=:0.0 && timeout 20s dillo -f -g 1920x1080 "+job["item"]+" 2>/dev/null"
		#_command="export DISPLAY=:0.0 && timeout 20s iceweasel -P avocado -height 1080 -width 1920 "+job["item"]+" 2>/dev/null"
		logger.info(_command)
		p = Popen(_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
		logger.info(re.sub('\\n+','',str(p.stdout.read().decode("utf-8"))))
		logger.error(re.sub('\\n+','',str(p.stderr.read().decode("utf-8"))))

		removeFromQ(avocadoQueueDir, jobname)

def listCache(avocadoCacheDir,html=False):

	contents, cachesize = getCContents(avocadoCacheDir)

        if html:
                print "<table>"
                for item in contents:
                        print "<tr>"
                        if str(contents[item]["type"]) == "youtube":
                                print '<td><img src="images/youtube.png"></td>'
                        elif str(contents[item]["type"]) == "webbrowse":
                                print '<td><img src="images/webbrowse.png"></td>'
                        print "<td>"+str(time.ctime(contents[item]["mtime"]))+"</td>"
                        print "<td>"+str(contents[item]["size"])+"</td>"
                        print "<td>"+str(contents[item]["item"])+"</td>"
                        print "<td>"+item+"</td>"
                        print "</tr>"
                print "</table>"
                print "<table>"
                print "<tr>"
                print "<td>Total Cache Size: "+cachesize+"</td>"
                print "</tr>"
                print "</table>"

        else:

                for item in contents:
                        print item+" "+str(contents[item]["mtime"])+" "+str(contents[item]["size"])+" "+str(contents[item]["type"])+" "+str(contents[item]["item"])



def listQ(avocadoQueueDir,html=False):

	contents = getQContents(avocadoQueueDir)

	if html:
		print "<table>"
		for item in contents:
			print "<tr>"
			if str(contents[item]["type"]) == "youtube":
				print '<td><img src="images/youtube.png"></td>'
                        elif str(contents[item]["type"]) == "webbrowse":
                                print '<td><img src="images/webbrowse.png"></td>'
			print "<td>"+item+"</td>"
			print "<td>"+str(contents[item]["mtime"])+"</td>"
			print "<td>"+str(contents[item]["type"])+"</td>"
			print "<td>"+str(contents[item]["timeout"])+"</td>"
			print "<td>"+str(contents[item]["item"])+"</td>"
			print "</tr>"
		print "</table>"

	else:

		for item in contents:
			print item+" "+str(contents[item]["mtime"])+" "+str(contents[item]["type"])+" "+str(contents[item]["timeout"])+" "+str(contents[item]["item"])

def main():

        parser = OptionParser()
        parser.add_option("-a", "--add", dest="add", help="add to avocado queue")
        parser.add_option("-t", "--type", dest="addtype", help="required for -a, type of item, valid-types: youtube, pics, video, webbrowse")
        parser.add_option("-o", "--timeout", dest="addtimeout", help="optional for -a, timeout of the added item, e.g. stop display of a webpage after 5m, for valid options see \"man timeout\", default is 30m")
        parser.add_option("-r", "--remove", dest="remove", help="remove from avocado queue")
	parser.add_option("-D", "--daemon", action="store_true", dest="daemon", default=False, help="start avocado queue worker daemon")
	parser.add_option("-s", "--start", action="store_true", dest="start", default=False, help="start next item and remove it from queue")
	parser.add_option("-k", "--kiosk", action="store_true", dest="kioskmode", default=False, help="repeats last items till new ones are added.")
	parser.add_option("--remove-kiosk", action="store_true", dest="removekiosk", default=False, help="flush the kiosk queue")
	parser.add_option("--html", action="store_true", dest="htmloutput", default=False, help="generate html output")
	parser.add_option("-l", "--list", action="store_true", dest="list", default=False, help="list avocado queue")
	parser.add_option("-c", "--list-cache", action="store_true", dest="listcache", default=False, help="list (youtube) cached files")
        (options, args) = parser.parse_args()

	avocadoUser="pi"
	avocadoGroup="www-data"

	try:
		avocadoUid=getpwnam(avocadoUser).pw_uid
		avocadoGid=getpwnam(avocadoGroup).pw_uid
	except:
		logger.info("user or group not found: "+avocadoUser+" "+avocadoGroup)
		avocadoUid=0
		avocadoGid=0


	avocadoDir="/var/lib/avocado/"
	avocadoWebDir="/var/www/"
	avocadoQueueDir="/var/lib/avocado/queue/"
	avocadoKioskQueueDir="/var/lib/avocado/kioskqueue/"
	avocadoCacheDir="/var/lib/avocado/cache/"
	avocadoCacheValidateDir="/var/lib/avocado/cache_validate/"


	if not os.path.isdir(avocadoDir):
		os.makedirs(avocadoDir)
		os.makedirs(avocadoQueueDir)
		os.makedirs(avocadoKioskQueueDir)
		os.makedirs(avocadoCacheDir)
		os.makedirs(avocadoCacheValidateDir)
		os.makedirs(avocadoWebDir)
		os.chown(avocadoDir, avocadoUid, avocadoGid)
		os.chown(avocadoQueueDir, avocadoUid, avocadoGid)
		os.chown(avocadoKioskQueueDir, avocadoUid, avocadoGid)
		os.chown(avocadoCacheDir, avocadoUid, avocadoGid)
		os.chown(avocadoCacheValidateDir, avocadoUid, avocadoGid)

		if os.path.isdir(avocadoQueueDir):
			logger.info(avocadoDir+" created.")
		else:
			logger.info(avocadoDir+" does not exists and creation failed, exiting.")
			sys.exit(1)	

	_type=None

	if options.daemon:
		#realDaemon(avocadoDir, avocadoWebDir, avocadoQueueDir, avocadoCacheDir, avocadoCacheValidateDir, avocadoKioskQueueDir, options.kioskmode)
		avocadoDaemon(avocadoDir, avocadoWebDir, avocadoQueueDir, avocadoCacheDir, avocadoCacheValidateDir, avocadoKioskQueueDir, options.kioskmode)

	if not options.addtimeout:
		_timeout="30m"
	else:
		_timeout=options.addtimeout

	if options.removekiosk:
		try:
			dirf = glob.glob(avocadoKioskQueueDir+"*")
			for file in dirf:
				os.unlink(file)
			sys.exit(0)
		except:
			sys.exit(1)

	if options.add and options.addtype:

		if options.addtype == "youtube":
			_type="youtube"
		elif options.addtype == "pics":
			_type="pics"
		elif options.addtype == "video":
			_type="video"
		elif options.addtype == "webbrowse":
			_type="webbrowse"

		if not _type:
			logger.error("unkown type: "+options.addtype+" for "+options.add)		
			sys.exit(1)

		addToQ(avocadoQueueDir, avocadoKioskQueueDir, options.add, _type, _timeout) 

	elif options.list:
		listQ(avocadoQueueDir,options.htmloutput)

	elif options.listcache:
		listCache(avocadoCacheDir,options.htmloutput)

	elif options.remove:
		removeFromQ(avocadoQueueDir, options.remove)

	elif options.start:
		nextInQ(avocadoQueueDir,avocadoCacheDir,avocadoCacheValidateDir,avocadoDir,avocadoWebDir, avocadoKioskQueueDir, options.kioskmode)


	else:
		logger.error("invalid arguments.")
		sys.exit(2)





if __name__ == '__main__':
        main()
