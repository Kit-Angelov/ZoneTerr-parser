from docx import Document
import os


def fill_docx(file, path_to_tempalate, path_to_save=os.getcwd(), **kwargs):
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)
    temp = {'number': "<номер>",
            'name': '<наименование>',
            'name_file': '<имя файла>',
            'size': '<размер>'}
    if os.path.exists(path_to_tempalate):
        doc = Document(path_to_tempalate)
        for i in doc.paragraphs:
            style = i.style
            for key in temp.keys():
                if i.text.find(temp[key]) != -1:
                    try:
                        i.text = str(i.text).replace(temp[key], str(kwargs[key]))
                        doc.save(os.path.join(path_to_save, '{0}.docx'.format(file)))
                        i.style = style
                    except KeyError:
                        print('Не переданы нужные ключи')
    else:
        print('путь до шаблона неверный')


if __name__ == '__main__':
    fill_docx(file='first7',
              path_to_tempalate='template-doc\Заявление в ГКНШаблон.docx',
              path_to_save='stat_docx',
              number='sdf',
              name=33,
              name_file='43',
              size='ee')
