# tweepy_scripts

Scripts to get data from Twitter using tweepy https://github.com/tweepy/tweepy
Note that, for the code to support multiple authentication handlers, one has to use the fork 
of tweepy by nirg: https://github.com/nirg/tweepy. The latter allows us to use multiple twitter 
accounts/applications in order to get around the rate limit.

- graph_generation.py gets a Twitter graph with n nodes starting from given id. 
- optimize_graph.py optimizes a given graph by recursively removing the node with 
minimal number of edges until reaching a given number of remaining nodes. 
- get_tweets.py takes a list of users and for evrey user it gets his/her most 
recent given number of tweets. 
  

