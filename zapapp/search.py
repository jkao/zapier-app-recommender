#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import json
import logging
import nltk
import re

"""
    Search interface for the app
"""
class ZapSearch():

    def __init__(self, esUrl, cleaner, appNames='names.json', categoriesPath='categories.json'):
        self.cleaner = cleaner

        # open entity lists
        with open(appNames) as f:
            self.appNames = json.load(f)
        with open(categoriesPath) as f:
            self.categories = json.load(f)

        # create a normalized map for app names and categories
        # maybe introduce notion of aliases in the future
        self.appNamesMap = {}
        for n in self.appNames:
            key = self.cleaner.normalizeString(n)
            unspacedKey = key.replace(' ', '')
            self.appNamesMap[key] = n
            self.appNamesMap[unspacedKey] = n

        self.categoriesMap = {}
        for n in self.categories:
            key = self.cleaner.normalizeString(n)
            unspacedKey = key.replace(' ', '')
            self.categoriesMap[key] = n
            self.categoriesMap[unspacedKey] = n

        # Elasticsearch
        bonsai = esUrl
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

    def search(self, query):
        normalized = self.cleaner.normalizeString(query)

        tokenized = nltk.word_tokenize(normalized)
        bigrams = nltk.ngrams(tokenized, 2)

        appNames = self.extractAppNames(tokenized, bigrams)
        categories = self.extractCategories(tokenized, bigrams)

        #logging.info('Query: ' + normalized + ' appNames: ' + str(appNames) + ' categories: ' + str(categories))
        print('Query: ' + normalized + ' appNames: ' + str(appNames) + ' categories: ' + str(categories))

        return self.fetch(normalized, appNames, categories)

    def extractAppNames(self, unigrams, bigrams):
        appNames = set([])
        for u in unigrams:
            if self.appNamesMap.get(u):
                appNames.add(self.appNamesMap[u])

        for b in bigrams:
            word = ' '.join(b)
            if self.appNamesMap.get(word):
                appNames.add(self.appNamesMap[word])

        return appNames

    def extractCategories(self, unigrams, bigrams):
        categories = set([])
        for u in unigrams:
            if self.categoriesMap.get(u):
                categories.add(self.categoriesMap[u])

        for b in bigrams:
            word = ' '.join(b)
            if self.categoriesMap.get(word):
                categories.add(self.categoriesMap[word])

        return categories

    def fetch(self, normalizedQuery, appNames, categories, offset=0, limit=10):
        shouldQueries = [
            { 'match': { 'serviceSummary': { 'query': normalizedQuery, 'boost': 2.0 } } },
            { 'match': { 'zapRecipes': normalizedQuery } },
            { 'match': { 'triggersAndActionStrings': normalizedQuery } },
            { 'match': { 'reviewStrings': { 'query': normalizedQuery, 'boost': 1.4 } } },
            { 'match': { 'appCopySectionStrings': { 'query': normalizedQuery, 'boost': 1.3 } } },
        ]

        # improve precision for app names
        for n in (appNames or []):
            shouldQueries.append({ 'match': { 'appName': { 'query': n, 'boost': 4.5 } }  })

        # improve precision for categories
        for c in (categories or []):
            shouldQueries.append({ 'match': { 'classes': { 'query': c, 'boost': 1.3 } }  })

        results = self.es.search(
            index = 'zap',
            doc_type = 'apps',
            body = {
                'query': {
                    'function_score': {
                        'query': {
                            'dis_max': {
                                'queries': [
                                    { 'bool': { 'should': [shouldQuery] }}
                                    for shouldQuery
                                    in shouldQueries
                                ]
                            },
                        },
                        'functions': [
                            {
                                'script_score': {
                                    'script': '_score * ((5 / doc["popularity"]))'
                                }
                            }
                        ]
                    }
                },
                'fields': ['appName', 'appHeroIntro', 'classes', 'link', 'reviewLink', 'serviceSummary', 'popularity']
            },
            from_ = offset,
            size = limit
        )

        return results
