import json

data = json.load(open('unis.json'))

for idx, uni in enumerate(data):
    for key, value in uni.items():
        if (isinstance(value, str)):
            new_value = value.replace('mailto:', '').strip().replace('\r', '').replace('\n\n', '\n').replace('/en', '')
            if new_value:
                uni[key] = new_value
            else:
                uni[key] = None
    uni["name"] = uni["name"].title().replace('University', 'Üniversitesi')

json.dump(data, open('out.json', 'w'), ensure_ascii=False)
