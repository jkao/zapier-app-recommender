import elasticsearch
import json
import re
import requests

"""
    Script to upload Zapier documents to ES service
"""
class ElasticSearchUpload():

    def __init__(self, inPath, serviceUrl):
        self.inPath = inPath
        self.serviceUrl = serviceUrl

        bonsai = self.serviceUrl
        auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
        host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

        esHeader = [{
            'host': host,
            'port': 443,
            'use_ssl': True,
            'http_auth': (auth[0], auth[1])
        }]

        self.es = elasticsearch.Elasticsearch(esHeader)
        assert(self.es.ping())

    def run(self):
        # load json files
        with open(self.inPath) as f:
            data = json.load(f)

        # upload it to ES
        for doc in data:
            print('Uploading...', doc['appName'])
            self.es.index(index='zap', doc_type='apps', body=doc)



if __name__ == '__main__':
    esUrl = argv[1]
    upload = ElasticSearchUpload(inPath='entries.json', serviceUrl=esUrl)
    upload.run()
