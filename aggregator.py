
data = {}


def aggregate(uniqueName, tag, epocTime):
    if uniqueName not in data:
        data[uniqueName] = {}
    if tag in data[uniqueName] and data[uniqueName][tag]['time'] == epocTime:
        data[uniqueName][tag] = {'count': data[uniqueName][tag]['count'] + 1, 'time': epocTime}
    else:
        data[uniqueName][tag] = {'count': 1, 'time': epocTime}
    return data