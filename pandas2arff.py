
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
                set_notation = '{' + ','.join(levels) + '}'
                f.write('@attribute {} {}'.format(set_notation))
            else:
                pass
                # TODO raise a stink

        f.write('@data\n')
        dataframe.to_csv(f, header=False)

