'''
This code was taken from contextminer and retrofitted for the socrates infrastructure

Right now this seems to get only the most recent
'''

import csv
import io
import logging
import urllib2
import urllib
import urlparse
try:
    import simplejson as json
except ImportError:
    import json
import urllib

SPECS = {
    "functions": {
        "search" : {
            "param" : {
                "query" : {
                    "type" : "text",
                    "comment" : "The query for the YouTube search"
                }
            },
            "returns" : {
                "title" : "text",
                "category" : "text",
                "url" : "text",
                "date_uploaded" : "text",
                "duration" : "numeric",
                "views" : "numeric"
            }
        }
    }
}

base_url = "https://gdata.youtube.com/"
logging.basicConfig(level=logging.DEBUG)

def _make_url(endpoint, **kwargs):
    url = '%s?%s' % (
	urlparse.urljoin(base_url, endpoint),
	urllib.urlencode(_fix_kwargs(kwargs))
    )
    return url

def _fix_kwargs(kwargs):
    """
    Remove kwargs that are None
    """
    return dict([(k, v) for k, v in kwargs.items() if v != None])

def _request(url, data=None):
    """
    If data is None, makes a GET request, else makes a POST request
    """
    res = urllib2.urlopen(url, data)
    return json.loads(res.read())

def name():
    """
    Returns the human-readable name of this source
    """
    return "YouTube Search"

def list_attrs():
    """
    Returns a list of attributes that this miner can mine
    """
    return []

def to_csv(data):
    result = io.BytesIO()
    writer = csv.writer(result)
    writer.writerow(['Title', 'Author', 'Published', 'Category', 
		     'Description', 'Video'])
    for d in data:
	if 'mediagroup' in d['data']:
	    description = d['data'].get('mediagroup').get('mediadescription').get('t').encode('ascii', 'backslashreplace')
	else:
	    description = ''

	writer.writerow([d['data']['title']['t'].encode('ascii', 'backslashreplace'), 
			', '.join([a['name']['t'] for a in d['data']['author']]), 
			d['data']['published']['t'],
			', '.join([c['label'] for c in d['data']['category'] if 'label' in c]),
			description,
			d['data']['content']['src'].encode('ascii', 'backslashreplace')])

    return [('youtube_search', result.getvalue())]

def ysearch(**kwargs):
    """
    Queries the search endpoint with given params. Query to search for is found
    in the q param. 
    """
    result = []
    url = _make_url('/feeds/api/videos', **kwargs)
    for i in range(1): #the 1 can be increased to add additional results
	logging.debug("url: " + url)
	res = _request(url)
	if not res:
	    break
	#logging.debug(res)
	if not 'entry' in res['feed']:
	    break
	else:
	    result.extend(res['feed']['entry'])

	# find the next url
	nurl = ''
	for link in res['feed']['link']:
	    if link['rel'] == 'next':
		nurl = link['href']
	if not nurl:
	    break
	else: 
	    url = nurl
    return result

def search(param):
    query = param['query']
    objs = ysearch(q=query, orderby="published", alt="json", v=2, time="today")
    #make objects a little nicer and flatter
    result = []
    for o in objs:
        cat = ""
        if "category" in o:
            for c in o["category"]:
                if "label" in c:
                    cat = c["label"]
                    break
        views = 0
        if "yt$statistics" in o:
            views = o["yt$statistics"]["viewCount"]
        r = {
            "title" : o["title"]["$t"],
            "category" : cat,
            "url" : o["media$group"]["media$player"]["url"],
            "date_uploaded" : o["media$group"]["yt$uploaded"]["$t"],
            "duration" : float(o["media$group"]["yt$duration"]["seconds"]),
            "views" : int(views)
        }
        result.append(r)
    return result