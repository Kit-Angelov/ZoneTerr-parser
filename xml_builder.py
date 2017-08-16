import sys
import os
import argparse
from getCadDist import CadastralDistrict
from tz_builder import tz_build


def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise Exception("Ошибка обращения к директории:{0} неверно указан путь".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise Exception("Ошибка обращения к директории:{0} нет доступа".format(prospective_dir))

parser = argparse.ArgumentParser(description='Конструктор XML')
parser.add_argument('-i',
                    dest='input',
                    help='путь к директории с исходными данными',
                    nargs='?',
                    type=readable_dir,
                    )
parser.add_argument('-o',
                    dest='output',
                    help='путь к директории результата',
                    nargs='?',
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '!result')
                    )
parser.add_argument('-t',
                    dest='template',
                    help='путь к директории шаблонов',
                    nargs='?',
                    type=readable_dir,
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template-doc')
                    )
parser.add_argument('-f',
                    dest='fias',
                    help='Сервис ФИАС (для определения класс.кодов адреса)',
                    default='http://192.168.2.76:8000/api/addr_obj/{0}/'
                    )
parser.add_argument('-c',
                    dest='cad_dis',
                    help='Директория содержащая коды регионов ',
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CadastralDistrict')
                    )

print(parser)
args = parser.parse_args()

if __name__ == '__main__':
    tz_build(input=args.input, output=args.output, template=args.template, fias_service=args.fias, cd=CadastralDistrict(args.cad_dis))
