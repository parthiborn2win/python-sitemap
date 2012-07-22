import re
import mechanize
import sys

br = mechanize.Browser()
sitename = "http://%s" %(sys.argv[1])

br.open("%s/" %(sitename))
# follow second link with element text matching regular expression
response1 = br.follow_link(text_regex=r"/*", nr=1)
assert br.viewing_html()

links = []
for link in br.links(url_regex="/*"):
    #print link.url
    links.append(link.url)
    br.follow_link(link)  # takes EITHER Link instance OR keyword args
    br.back()
    
links = list(set(links))

print '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'''

try:
    for link in links:
        if not link == "/":
            br.open("%s%s" %(sitename,link))
            br.links(url_regex="/*")
            for blink in br.links(url_regex="/*"):
                if blink.url not in links:
                    #print blink.url
                    links.append(blink.url)
except:
    pass
    
links = list(set(links))
for link in links:
    if link[0] == "/":
        print "<url><loc>%s%s</loc><changefreq>daily</changefreq><priority>1.00</priority></url>" %(sitename,link)
print '</urlset>'
