
def dataframe2arff(dataframe, filename, coltypes, relation, include_index=False):
    if include_index:
        dataframe = dataframe.reset_index()
        
    with open(filename, 'w') as f:
        f.write('@relation {}\n'.format(relation))
        
        for column in dataframe:
            attrtype = coltypes[column]
            # TODO input validation
            if attrtype == 'numeric':
                f.write('@attribute {} numeric\n'.format(column))
            elif attrtype == 'string':
                f.write('@attribute {} string\n'.format(column))
            elif attrtype == 'nominal':
                levels = dataframe[column].unique()
                set_notation = '{' + ','.join(map(str, levels)) + '}'
                f.write('@attribute {} {}\n'.format(column, set_notation))
            else:
                pass
                # TODO raise a stink

        f.write('@data\n')
        dataframe.to_csv(f, header=False, index=False)

import pandas
import StringIO as io
import re
relation = r'@relation (?P<relation>[^\n]+)'
attribute = r'@attribute (?P<attribute>[^\n]+)'
data = r'@data\n(?P<data>.+)'
arff_re = re.compile(r'{}|{}|{}'.format(relation, attribute, data), re.DOTALL)

def arff2dataframe(filename):
    with open(filename, 'r') as f:
        text = f.read()
    column_names = []
    for m in arff_re.finditer(text):
        d = m.groupdict()
        if d['attribute']:
            colm = re.match(r'\'(.+)\'|(\w+)', d['attribute'])
            column_names.append(colm.group(1) or colm.group(2))
        if d['data']:
            csv_data = d['data']
    return pandas.read_csv(io.StringIO(csv_data),
                           header=None,
                           names=column_names)
