


"""
    Получение данных из локальной базы базы ФИАС
"""
    name_line = data_dict['address'].replace(',', '').replace(' ', '_')
    text = quote('{0}'.format(name_line))
    r = urllib.request.urlopen(fias_service.format(text))
    data = json.loads(r.read().decode('utf-8'))
    data.update(data_dict)