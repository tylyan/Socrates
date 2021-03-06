#5 Different methods of searching comments on NY Times
#RECENT xml error
#RANDOM xml error
#DATE 
#USER ID
#URL

import urllib, urllib2
import simplejson as json

SPECS = {
	'description' : 'Fetching comments from NY Times',
	'functions': {
		'comments_by_URL':{
			'param': {
				"submission_url" : {
					"type" : "text",
					"comment" : "URL of post (ends with .html)"
				},
				"sort" : {
					"type" : "text",
					"constraints" : {
						"choices" : ["newest", "oldest", "recommended", "replied", "editors-selection"]
					},
					"default" : "newest"
				}
			},
			'returns': {
				'approveDate': "text",
				'commentBody': "text",
				'commentSequence': "numeric",
				#'commentTitle': "text", #usually empty
				'display_name': "text",
				'editorsSelection': "boolean",
				#'email_status': "text", #usually 0
				'location': "text",
				'recommendations': "numeric",
				#'replies': "array", #usually undefined
				'sharing': "numeric",
				#'status': "text", #usually approved
				'times_people': "numeric",
				'userComments': "text",
				#'userTitle': "text", #usually undefined
				#'userURL': "text" #usually undefined
			}
		},
		'article_search' : {
			'param' : {
				'query' : {
					"type" : "text",
					"comment" : "Search query"
				},
				"sort" : {
					"type" : "text",
					"constraints" : {
						"choices" : ["newest", "oldest"]
					},
					"default" : "newest"
				}				
			},
			'returns' : {
				"web_url" : "text",
				"headline" : "text",
				"abstract" : "text",
				"word_count" : "numeric",
				"lead_paragraph" : "text", 
				"snippet" : "text"
			}
		}#,
		#'comments_by_Date':{
		#	'param': {
		#		"date" : {
		#			"type" : "text",
		#			"comment" : "YYYYMMDD"
		#		}	
		#	},
		#	'returns': {
		#		'approveDate': "text",
		#		'commentBody': "text",
		#		'commentSequence': "numeric",
		#		#'commentTitle': "text", #usually empty
		#		'display_name': "text",
		#		'editorsSelection': "boolean",
		#		#'email_status': "text", #usually 0
		#		'location': "text",
		#		'recommendations': "numeric",
		#		#'replies': "array", #usually undefined
		#		'sharing': "numeric",
		#		#'status': "text", #usually approved
		#		'times_people': "numeric",
		#		'userComments': "text",
		#		#'userURL': "text" #usually undefined
		#	}
		#}
	}
}
	
def comments_by_URL(param):
	matchtype = "exact-match"
	cosearch = "http://api.nytimes.com/svc/community/v2/comments/url/"+matchtype+".json?"
	url = param['submission_url'].strip()
	sort = param['sort']
	key = "d7064151a6a66f53a361ba89b0d5d0b6:8:69414651"

	q = {"url":url, "sort":sort, "api-key":key}
	url = cosearch+urllib.urlencode(q)

	def call_the_articles():
		result = urllib2.urlopen(url).read()
		return json.loads(result)
		
	articles = call_the_articles()
	commentList = []
	for comments in articles['results']['comments']:
		cObj = {
			'approveDate': comments['approveDate'],
			'commentBody': comments['commentBody'],
			'commentSequence': comments['commentSequence'],
			'commentTitle': comments['commentTitle'],
			'display_name': comments['display_name'],
			'editorsSelection': comments['editorsSelection'],
			'email_status': comments['email_status'],
			'location': comments['location'],
			'recommendations': comments['recommendations'],
			'sharing': comments['sharing'],
			'status': comments['status'],
			'times_people': comments['times_people'],
			'userComments': comments['userComments'],
		}
		commentList.append(cObj)
	return commentList

def article_search(param):
	arsearch = "http://api.nytimes.com/svc/search/v2/articlesearch.json?"
	query = param['query']
	sort = param['sort']
	key = "688a998952b3b054ef2cbf264a8d1fc7:8:69414651"
	q = {"q":query, "sort": sort, "api-key":key}
	url = arsearch+urllib.urlencode(q)

	def call_the_articles():
		result = urllib2.urlopen(url).read()
		return json.loads(result)

	articles = call_the_articles()
	articleList = []
	for docs in articles['response']['docs']:
		aObj = {
			'web_url': docs['web_url'],
			'headline': docs['headline']['main'],
			'abstract': docs['abstract'],
			'word_count': int(docs['word_count']),
			'lead_paragraph': docs['lead_paragraph'],
			'snippet': docs['snippet']
		}
		articleList.append(aObj)
	return articleList


#def comments_by_Date(param):
#	date = param['date']
#	cosearch = "http://api.nytimes.com/svc/community/v2/comments/by-date/" + date + ".json?"
#	key = "d7064151a6a66f53a361ba89b0d5d0b6:8:69414651"
#
#	q = {"api-key":key}
#	url = cosearch+urllib.urlencode(q)
#
#	def call_the_articles():
#	    result = urllib2.urlopen(url).read()
#	    return json.loads(result)
#
#	articles = call_the_articles()
#	commentList = []
#	for comments in articles['results']['comments']:
#		cObj = {
#			'approveDate': comments['approveDate'],
#			'commentBody': comments['commentBody'],
#			'commentSequence': comments['commentSequence'],
#			'commentTitle': comments['commentTitle'],
#			'display_name': comments['display_name'],
#			'editorsSelection': comments['editorsSelection'],
#			'email_status': comments['email_status'],
#			'location': comments['location'],
#			'recommendations': comments['recommendations'],
#			'sharing': comments['sharing'],
#			'status': comments['status'],
#			'times_people': comments['times_people'],
#			'userComments': comments['userComments'],
#		}
#		commentList.append(cObj)
#	return commentList