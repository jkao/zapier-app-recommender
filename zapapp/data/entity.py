import json

"""
    Script to denormalize category and app names
"""
class EntityExtractor():

    def __init__(self, inPath='entries.json', categoriesPath='categories.json', namesPath='names.json'):
        self.inPath = inPath
        self.categoriesPath = categoriesPath
        self.namesPath = namesPath

    def run(self):
        # load json
        with open(self.inPath) as f:
            data = json.load(f)

        names = set([])
        categories = set([])

        for entry in data:
            if entry['appName']:
                names.add(entry['appName'])
            if entry['classes']:
                for c in entry['classes']:
                    categories.add(c)

        # save json files
        with open(self.categoriesPath, 'w') as f:
            json.dump(list(categories), f)
        with open(self.namesPath, 'w') as f:
            json.dump(list(names), f)


if __name__ == '__main__':
    ee = EntityExtractor(
            inPath='entries.json',
            categoriesPath='categories.json',
            namesPath='names.json'
        )
    ee.run()
