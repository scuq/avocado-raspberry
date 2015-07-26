avocado creates a queue of avocado-items (youtube, webbrowse, local picture show)

youtube vids are downloaded with cclive and played with omxplayer
you need enough diskspace because the vids are cached in the avocado cache dir

webbrowse launches midori and display the page for the given time (timeout) default is 30 minutes

local pictures are displayed with qiv, all pictures have to be in one directory (can be filled with samba)

if you enable the --kiosk(mode) avocado keeps playing and displaying the previous items randomly
till you add new ones or the pi is burning

for your convenience the avocado queue can be viewed and filled by a simple webinterface running on lighttpd with php5-cgi