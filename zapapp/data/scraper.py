import bs4
import json
import sys
import urllib2

"""
    Zapbook scraped entry that gets iteratively populated
"""
class ZapbookEntry():

    def __init__(self, entryHtml, appName, title, link, classes, popularity):
        # 1st stage of pipeline: zapbook list content
        self.entryHtml = entryHtml
        self.appName = appName
        self.title = title
        self.link = link
        self.classes = classes
        self.popularity = popularity

        # 2nd stage of pipeline: zapbook entry content
        self.appHeroIntro = None
        self.zapRecipes = None
        self.appCopySectionStrings = None
        self.reviewLink = None
        self.triggersAndActionsStrings = None

        # 3rd stage of pipeline: zapbook review content
        self.serviceSummary = None
        self.reviewStrings = None

    def toDict(self):
        return {
            'appName': self.appName,
            'title': self.title,
            'link': self.link,
            'classes': self.classes,
            'appHeroIntro': self.appHeroIntro,
            'zapRecipes': self.zapRecipes,
            'appCopySectionStrings': self.appCopySectionStrings,
            'reviewLink': self.reviewLink,
            'triggersAndActionsStrings': self.triggersAndActionsStrings,
            'serviceSummary': self.serviceSummary,
            'reviewStrings': self.reviewStrings,
            'popularity': int(self.popularity)
        }


"""
    Script to scrape data from Zapier's site (sorry!)
"""
class ZapbookScraper():

    def __init__(self, outPath='entries.2.json'):
        self.outPath = outPath

    def run(self):
        # STAGE 1: fetch entries from https://zapier.com/zapbook/
        print("stage 1")
        entries = self.fetchZapbookEntries()

        # STAGE 2: fetch content from https://zapier.com/zapbook/$ENTRY
        print("stage 2")
        entries = [self.fetchZapbookEntryContent(e) for e in entries]

        # STAGE 3: fetch content from https://zapier.com/zapbook/$ENTRY/review/
        print("stage 3")
        reviewedEntries = [self.fetchZapbookReview(e) for e in entries]

        # Output
        entriesJson = [e.toDict() for e in entries]
        with open(self.outPath, 'w') as outfile:
            json.dump(entriesJson, outfile)

        return entries

    def fetchZapbookEntries(self):
        zapbooksUrl = 'https://zapier.com/zapbook/'
        response = urllib2.urlopen(zapbooksUrl)
        html = response.read()
        soupResponse = bs4.BeautifulSoup(html)

        servicesHtml = soupResponse.find_all('li', class_='service')
        services = []

        filteredClasses = set([
            'service',
            'app-picker-item',
            'service-all',
        ])

        for html in servicesHtml:
            classes = []
            if html.attrs['class']:
                classes = [
                    c.replace('service-', '') for c in html.attrs['class']
                    if c not in filteredClasses
                ]

            aTag = html.find('a')
            href = aTag.attrs['href']
            title = aTag.attrs['title']

            appNameTag = aTag.find('p', class_='app-name')
            appName = appNameTag.text

            popularity = html.attrs['data-popularity']

            entry = ZapbookEntry(html, appName, title, href, classes, popularity)
            services.append(entry)

        return services

    def fetchZapbookEntryContent(self, zapbookEntry):
        if not zapbookEntry:
            return zapbookEntry
        if not zapbookEntry.link:
            return zapbookEntry

        # load the page
        baseUrl = 'https://zapier.com'
        fullUrl = baseUrl + zapbookEntry.link
        print("zapbook entry content", fullUrl)

        response = urllib2.urlopen(fullUrl)
        html = response.read()
        content = bs4.BeautifulSoup(html)

        # app hero intro
        appHeroIntroTag = content.find('h4', class_='app-hero-intro')
        appHeroIntro = None
        if appHeroIntroTag:
            appHeroIntro = appHeroIntroTag.text

        zapbookEntry.appHeroIntro = appHeroIntro

        # zap recipe
        zapRecipeTags = content.find_all('div', class_='popular-zap-bottom') or []
        zapRecipes = [pop.find('p').text for pop in content.find_all('div', class_='popular-zap-bottom')]

        zapbookEntry.zapRecipes = zapRecipes

        # app copy
        appCopySectionTag = content.find('div', class_='app-copy-section')
        appCopySectionStrings = []
        if appCopySectionTag:
            appCopySectionStrings = list(appCopySectionTag.stripped_strings)

        zapbookEntry.appCopySectionStrings = appCopySectionStrings

        # review link
        reviewLink = None
        if appCopySectionTag:
            reviewTag = appCopySectionTag.find('a', class_='service-page-link')
            if reviewTag and reviewTag.attrs['href']:
                reviewLink = reviewTag.attrs['href']

        zapbookEntry.reviewLink = reviewLink

        # triggers & actions
        triggersAndActionsTag = content.find('div', 'triggers-and-actions__one-app')
        triggersAndActionsStrings = []
        if triggersAndActionsTag:
            triggersAndActionsStrings = list(triggersAndActionsTag.stripped_strings)

        zapbookEntry.triggersAndActionsStrings = triggersAndActionsStrings

        return zapbookEntry

    def fetchZapbookReview(self, zapbookEntry):
        if not zapbookEntry:
            return
        if not zapbookEntry.reviewLink:
            return

        # load the page
        baseUrl = 'https://zapier.com'
        fullUrl = baseUrl + zapbookEntry.reviewLink
        print('fetchZapbookReview ', fullUrl)

        try:
            response = urllib2.urlopen(fullUrl)
            html = response.read()
            content = bs4.BeautifulSoup(html)
        except:
            print("Womp womp ("+ fullUrl + ")", sys.exc_info()[0])
            return

        # service summary
        serviceSummary = content.find('div', class_='service-summary')
        if serviceSummary:
            zapbookEntry.serviceSummary = serviceSummary.text

        # features & review
        reviewTags = content.find_all('div', class_='review')
        reviewStrings = []
        if reviewTags:
            for tag in reviewTags:
                reviewStrings.extend(list(tag.stripped_strings))
            zapbookEntry.reviewStrings = reviewStrings

        return zapbookEntry


if __name__ == "__main__":
    zs = ZapbookScraper(outPath = 'entries.json')
    zs.run()
