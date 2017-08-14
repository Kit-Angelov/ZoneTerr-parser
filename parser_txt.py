import os
import urllib.request
from urllib.parse import quote
import json
from lxml import etree
import math
import uuid
import datetime
import sys
from shutil import copyfile

ns_TerritoryToGKN = {
            'xmlns': "urn://x-artefacts-rosreestr-ru/incoming/territory-to-gkn/1.0.4",
            'xmlns_ki3': "urn://x-artefacts-rosreestr-ru/commons/complex-types/cadastral-engineer/4.1.1",
            'xmlns_fio': "urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1",
            'xmlns_spat2': "urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/2.0.1",
            'xmlns_doci2': "urn://x-artefacts-rosreestr-ru/commons/complex-types/document-info/5.0.1",
        }

ns_ZoneToGKN = {
            'xmlns': "urn://x-artefacts-rosreestr-ru/incoming/zone-to-gkn/5.0.8",
            'xmlns_loc3': "urn://x-artefacts-rosreestr-ru/commons/complex-types/address-input/6.0.1",
            'xmlns_org3': "urn://x-artefacts-rosreestr-ru/commons/complex-types/organization/4.0.1",
            'xmlns_zone2': "urn://x-artefacts-rosreestr-ru/commons/complex-types/zone/4.2.2",
            'xmlns_fl3': "urn://x-artefacts-rosreestr-ru/commons/complex-types/person/5.0.2",
            'xmlns_fio': "urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1",
            'xmlns_doci2': "urn://x-artefacts-rosreestr-ru/commons/complex-types/document-info/5.0.1",
            'xmlns_dcl2': "urn://x-artefacts-rosreestr-ru/commons/complex-types/sender/5.0.1",
        }

pathToTerritoryToGKN = 'шаблон\TerritoryToGKN.xml'
pathToZoneToGKN = 'шаблон\ZoneToGKN.xml'

"""
Открытие txt ФАЙЛОВ
"""


def add_ordinate(parent_elem, NumGeopoint, X, Y, data):
    spelement_unit = etree.SubElement(parent_elem,
                                      '{%s}SpelementUnit' % ns_TerritoryToGKN['xmlns_spat2'],
                                      TypeUnit=data['TypeUnit'])

    ordinate = etree.SubElement(spelement_unit,
                                '{%s}Ordinate' % ns_TerritoryToGKN['xmlns_spat2'],
                                GeopointZacrep=data['GeopointZacrep'],
                                NumGeopoint=NumGeopoint,
                                X=X,
                                Y=Y,
                                DeltaGeopoint=data['DeltaGeopoint'],
                                GeopointOpred=data['GeopointOpred'])


def add_sub_eleme(root, data):
    """
    Формирование списка ординат
    """
    SpatialElement = root.xpath('//xmlns:EntitySpatial/xmlns_spat2:SpatialElement', namespaces=ns_TerritoryToGKN)
    SpatialElement[0].getparent().remove(SpatialElement[0])

    Borders = root.xpath('//xmlns:EntitySpatial/xmlns_spat2:Borders', namespaces=ns_TerritoryToGKN)
    Borders[0].getparent().remove(Borders[0])

    count = len(data['ordinate'])

    if count > 0:
        EntitySpatial = root.xpath('//xmlns:EntitySpatial', namespaces=ns_TerritoryToGKN)
        SpatialElement = etree.SubElement(EntitySpatial[0], '{%s}SpatialElement' % ns_TerritoryToGKN['xmlns_spat2'])
        Borders = etree.SubElement(EntitySpatial[0], '{%s}Borders' % ns_TerritoryToGKN['xmlns_spat2'])
        i = 1
        for item in data['ordinate']:
            X, Y, NumGeopoint = item.split(' ')
            add_ordinate(SpatialElement, NumGeopoint, X, Y, data)


def parse_territory_to_gkn(parser, data, directory, result_directory):
    """
    Парсинг по шаблону TerritoryToGKN
    """

    guid = uuid.uuid4()

    os.mkdir(result_directory + '\\' + str(guid))

    tree = etree.parse(pathToTerritoryToGKN, parser)
    root = tree.getroot()

    area = root.xpath('//xmlns:Area/xmlns:AreaMeter/xmlns:Area', namespaces=ns_TerritoryToGKN)
    area[0].text = data['area']

    inaccuracy = root.xpath('//xmlns:Area/xmlns:AreaMeter/xmlns:Inaccuracy', namespaces=ns_TerritoryToGKN)
    inaccuracy[0].text = str(int(round(math.sqrt(int(data['area'])) * 0.1 * 2, 0)))

    coord_systems = root.xpath('//xmlns:CoordSystems/xmlns_spat2:CoordSystem', namespaces=ns_TerritoryToGKN)
    coord_systems[0].set('CsId', str(guid))

    entity_spatial = root.xpath('//xmlns:EntitySpatial', namespaces=ns_TerritoryToGKN)
    entity_spatial[0].set('EntSys', str(guid))

    applied_file = root.xpath('//xmlns:Diagram/xmlns:AppliedFile', namespaces=ns_TerritoryToGKN)
    applied_file[0].set('Name', str(guid) + "\\" + directory + '_графика.pdf')

    root.set('GUID', str(guid))

    add_sub_eleme(root, data)

    etree.ElementTree(root).write('{0}\TerriotoryToGKN_{1}.xml'.format(result_directory, str(guid)), pretty_print=True, xml_declaration=True, encoding='utf-8')

    return str(guid)


def parse_zone_to_gkn(parser, data, directory, result_directory):
    """
        Парсинг по шаблону ZoneToGKN
    """
    guid = uuid.uuid4()

    os.mkdir(result_directory + '\\' + str(guid))

    tree = etree.parse(pathToZoneToGKN, parser)
    root = tree.getroot()

    name = root.xpath('//xmlns:Title/xmlns_doci2:Name', namespaces=ns_ZoneToGKN)
    name[0].text = str(directory)

    number = root.xpath('//xmlns:Title/xmlns_doci2:Number', namespaces=ns_ZoneToGKN)
    number[0].text = data['number']

    date = root.xpath('//xmlns:Title/xmlns_doci2:Date', namespaces=ns_ZoneToGKN)
    date[0].text = str(datetime.date.today())

    applied_file = root.xpath('//xmlns:Documents/xmlns:Document/xmlns_doci2:AppliedFile', namespaces=ns_ZoneToGKN)
    applied_file[0].set('Name', str(guid) + "\\" + directory + '.pdf')

    applied_file = root.xpath('//xmlns:Documents/xmlns:Document/xmlns_doci2:AppliedFile', namespaces=ns_ZoneToGKN)
    applied_file[1].set('Name', str(guid) + "\\" + 'Постановление_160.pdf')

    applied_file = root.xpath('//xmlns:Documents/xmlns:Document/xmlns_doci2:AppliedFile', namespaces=ns_ZoneToGKN)
    applied_file[2].set('Name', str(guid) + "\\" + 'Доверенность Палагин.pdf')

    applied_file = root.xpath('//xmlns:Documents/xmlns:Document/xmlns_doci2:AppliedFile', namespaces=ns_ZoneToGKN)
    applied_file[3].set('Name', str(guid) + "\\" + '3941 балансовая справка.pdf')

    CadastralDistrict = root.xpath('//xmlns:NewZones/xmlns:Zone/xmlns_zone2:CadastralDistrict', namespaces=ns_ZoneToGKN)
    #CadastralDistrict[0].text = str()

    code_zone_doc = root.xpath('//xmlns:NewZones/xmlns:Zone/xmlns_zone2:CodeZoneDoc', namespaces=ns_ZoneToGKN)
    code_zone_doc[0].text = str('Охранная зона ' + data['name_zone'] + ', адрес (местоположение): ' + data['address'])

    OKATO = root.xpath('//xmlns:NewZones/xmlns:Zone/xmlns_zone2:Locations/xmlns_zone2:Location/xmlns_loc3:OKATO',
                       namespaces=ns_ZoneToGKN)
    OKATO[0].text = str(data['okato'])

    KLADR = root.xpath('//xmlns:NewZones/xmlns:Zone/xmlns_zone2:Locations/xmlns_zone2:Location/xmlns_loc3:KLADR',
                       namespaces=ns_ZoneToGKN)
    KLADR[0].text = str(data['kladr'])

    OKTMO = root.xpath('//xmlns:NewZones/xmlns:Zone/xmlns_zone2:Locations/xmlns_zone2:Location/xmlns_loc3:OKTMO',
                       namespaces=ns_ZoneToGKN)
    OKTMO[0].text = str(data['oktmo'])

    PostalCode = root.xpath('//xmlns:NewZones/xmlns:Zone/xmlns_zone2:Locations/xmlns_zone2:Location/xmlns_loc3:PostalCode',
                       namespaces=ns_ZoneToGKN)
    PostalCode[0].text = str(data['postal_code'])

    Region = root.xpath('//xmlns:NewZones/xmlns:Zone/xmlns_zone2:Locations/xmlns_zone2:Location/xmlns_loc3:Region',
                       namespaces=ns_ZoneToGKN)
    Region[0].text = str(data['region'])

    District = root.xpath('//xmlns:NewZones/xmlns:Zone/xmlns_zone2:Locations/xmlns_zone2:Location/xmlns_loc3:District',
                        namespaces=ns_ZoneToGKN)
    District[0].set('Name', str(data['district']))

    SpecialZone = root.xpath('//xmlns:NewZones/xmlns:Zone/xmlns:SpecialZone/xmlns_zone2:ProtectedObject',
                          namespaces=ns_ZoneToGKN)
    SpecialZone[0].text = str('Охранная зона ' + data['name_zone'] + ', адрес (местоположение): ' + data['address'])

    Territory = root.xpath('//xmlns:NewZones/xmlns:Zone/xmlns:SpecialZone/xmlns:Territory/xmlns_doci2:AppliedFile',
                             namespaces=ns_ZoneToGKN)
    Territory[0].set('GUID', str(guid))
    Territory[0].set('Name', 'TerritoryToGKN_' + str(guid) + '.xml')

    root.set('GUID', str(guid))

    etree.ElementTree(root).write('{0}\ZoneToGKN_{1}.xml'.format(result_directory, str(guid)), pretty_print=True, xml_declaration=True, encoding='utf-8')

    return str(guid)


def main_func(path_to_files, path_result):
    """
    Главная функция
    """
    list_dirs = os.listdir(path_to_files)
    if not os.path.exists(path_result):
        os.mkdir(path_result)
    if len(list_dirs) > 0:
        for directory in list_dirs:
            list_files = os.listdir(path_to_files + directory)
            if len(list_files) > 0:
                for file in list_files:
                    if file.startswith('__tz_'):
                        data_dict = {}
                        with open(path_to_files + directory + '\\' + file, 'r') as txt:
                            result_directory = path_result + '\\' + directory
                            if not os.path.exists(result_directory):
                                os.mkdir(result_directory)
                            read_lines = txt.readlines()
                            text_semi_norm_arr = list(map(lambda x: x.replace('\n', ''), read_lines))
                            text_norm_arr = list(map(lambda x: x.replace('\t', ' '), text_semi_norm_arr))

                            info = text_norm_arr[0].split(' ')
                            data_dict['address'] = text_norm_arr[1]
                            data_dict['district'] = text_norm_arr[1].split(' ')[2]
                            data_dict['number'] = info[3]
                            data_dict['name_zone'] = text_norm_arr[0]
                            data_dict['file_name'] = str(dir)
                            data_dict['area'] = text_norm_arr[2]
                            data_dict['ordinate'] = [item for item in text_norm_arr[4:]]
                            data_dict['ordinate'].append(text_norm_arr[4])

                            ordinate_data = {}
                            if ordinate_data == {}:
                                data_dict['TypeUnit'] = 'Точка'
                                data_dict['GeopointZacrep'] = 'Закрепление отсутствует'
                                data_dict['DeltaGeopoint'] = '0.1'
                                data_dict['GeopointOpred'] = '692005000000'

                            print('data_dict: ', data_dict)

                            """
                                Получение данных из локальной базы базы ФИАС
                            """
                            name_line = data_dict['address'].replace(',', '').replace(' ', '_')
                            print('name_line: ', name_line)
                            text = quote('{0}'.format(name_line))
                            r = urllib.request.urlopen('http://192.168.2.185:8080/api/{0}/'.format(text))
                            data = json.loads(r.read().decode('utf-8'))
                            print('data: ', data)

                            data.update(data_dict)
                            print('all_data: ', data)

                            """
                                Парсинг данных в XML Шаблоны
                            """
                            parser = etree.XMLParser(ns_clean=True, remove_blank_text=True)
                            """
                                Парсинг по шаблону TerritoryToGKN.xml
                            """
                            territory_to_gkt_guid =parse_territory_to_gkn(parser, data, directory, result_directory)
                            """
                                Парсинг по шаблону ZoneToGKN.xml
                            """
                            zone_to_gkn_guid = parse_zone_to_gkn(parser, data, directory, result_directory)

                            """
                                Копирование файлов pdf в нашу директорию
                            """
                            for pdf_file in list_files:
                                if pdf_file.find('графика') != -1:
                                    copyfile((path_to_files + directory + '\\' + pdf_file),
                                             result_directory + '\\' + territory_to_gkt_guid + '\\' + pdf_file)
                                elif pdf_file.endswith('.pdf'):
                                    copyfile((path_to_files + directory + '\\' + pdf_file),
                                             result_directory + '\\' + zone_to_gkn_guid + '\\' + pdf_file)

"""        Мой никому не нужный убер-модуль для парсинга ОКАТО и КЛАДР

        # Работа с парсингом ОКТМО, КЛАДР, ОКАТО

        g = Grab()
        g.setup(proxy='192.168.2.28:8080', proxy_type='http')
        
        g.go('http://google.com/')
        g.set_input('q', 'Тамбовская область, Жердевский район site:kladr-rf.ru')
        g.submit()
        #print(g.response.unicode_body())
        #print(g.css_text('ul.breadcrumb strong em'))
        print('КЛАДР: ', g.xpath_text('//*[@class="breadcrumb"][2]//em'))
        print('Код региона : ', g.xpath_text('//*[@class="table table-bordered table-hover"]//td'))
        print('Почтовый индекс : ', g.xpath_text('//*[@class="table table-bordered table-hover"]//td[2]'))
        print('Код ОКАТО : ', g.xpath_text('//*[@class="table table-bordered table-hover"]//td[3]'))
"""

main_func('исх данные\\', 'result\\')






