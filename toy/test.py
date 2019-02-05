def test_kb():
    import toy.data as td
    print(td.KNOWLEDGE_BASE['park'])


def test_graph_model():
    pass
    # print(bgm.word2vec('this is a boss'))


def test_similarity():
    from similarity.ngram import NGram
    twogram = NGram(2)
    print(twogram.distance('ABCD', 'ABTUIO'))

    s1 = 'Adobe CreativeSuite 5 Master Collection from cheap 4zp'
    s2 = 'Adobe CreativeSuite 5 Master Collection from cheap d1x'
    fourgram = NGram(4)
    print(fourgram.distance(s1, s2))
    # print(twogram.distance(s1, s2))

    # s2 = 'Adobe CreativeSuite 5 Master Collection from cheap 4zp'
    # print(fourgram.distance(s1, s2))
    #
    # print(fourgram.distance('ABCD', 'ABTUIO'))

    print(1 - fourgram.distance(s1, s2))


def test_numpy_pandas_1():
    import numpy
    x = [[0, 0, 1], [1, 2, 2], [3, 4, 5]]
    y = numpy.array([numpy.array(xi) for xi in x])
    print(y)

    import pandas as pd
    dataframe = pd.DataFrame(data=y, columns=['one', 'two', 'three'], index=['a', 'b', 'c'])
    print(dataframe.to_string())

    print('1:', dataframe.columns.get_loc("one"))

    for index, row in dataframe.iterrows():
        print('2:', index, row)
        print()

    print('3:', dataframe.loc['a'])
    print('4:', dataframe.iloc[0])
    print()

    row = dataframe.loc['a']
    headers = list(dataframe.columns.values)
    for i in range(row.size):
        print('5:', headers[i], row[headers[i]])


def test_numpy_pandas_2():
    import numpy as np
    import pandas as pd
    x = [['a', 'b', 'c'], [0, 1, 2], [3, 4, 5]]
    data = np.array([np.array(xi) for xi in x])
    df = pd.DataFrame(data=data[1:, 0:], columns=data[0, 0:])
    print('6:', df.to_string())
    df.to_csv('test_file.csv', sep=',', encoding='utf-8')

    # import os
    # cwd = os.getcwd()
    # print(cwd)

    df2 = pd.read_csv('test_file.csv', index_col=0, header=0)
    print('7:', df2.to_string())


def test_rdf():
    from rdflib import Graph
    g1 = Graph()
    g1.parse("http://bigasterisk.com/foaf.rdf")
    len(g1)



    from rdflib import URIRef, BNode, Literal

    bob = URIRef("http://example.org/people/Bob")
    linda = BNode()

    name = Literal('Bob')
    age = Literal(24)
    height = Literal(76.5)

    # print(bob, linda, name, age, height)

    from rdflib.namespace import RDF, FOAF
    from rdflib import Graph
    g = Graph()

    g.add((bob, RDF.type, FOAF.Person))
    g.add((bob, FOAF.name, name))
    g.add((bob, FOAF.knows, linda))
    g.add((linda, RDF.type, FOAF.Person))
    g.add((linda, FOAF.name, Literal('Linda')))

    g.add((bob, FOAF.age, Literal(42)))
    print("Bob is ", g.value(bob, FOAF.age))

    g.set((bob, FOAF.age, Literal(43)))
    print("Bob is now ", g.value(bob, FOAF.age))

    g.serialize(format='turtle', destination='test_rdf.txt')

    g.remove((bob, None, None))
    g.serialize(format='turtle',destination='test_rdf2.txt')

    g = Graph()
    g.parse("test_rdf.txt", format='turtle')
    import pprint
    for stmt in g:
        pprint.pprint(stmt)

    return

def test_cosine_similarity():
    import re, math
    from collections import Counter

    WORD = re.compile(r'\w+')

    def get_cosine(vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(text):
        words = WORD.findall(text)
        return Counter(words)

    text1 = 'This is a foo bar sentence .'
    text2 = 'This sentence is similar to a foo bar sentence .'

    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    cosine = get_cosine(vector1, vector2)
    print(cosine)

def test_instance_matching():
    import numpy as np
    import pandas as pd
    tar = [['attr1', 'attr2', 'attr3'], ['aaaa', 'bbb', 'ccc'], ['xxx', 'yyyy', 'zzz']]
    # y = [['attr4', 'attr5', 'attr6'], ['xxx', 'yyy', 'zzz'], ['aaa', 'bbb', 'ccc']]
    src = [['attr4'], ['xxx'], ['aaa'], ['mmm']]

    data_tar = np.array([np.array(xi) for xi in tar])
    df_tar = pd.DataFrame(data=data_tar[1:, 0:], columns=data_tar[0, 0:])

    data_src = np.array([np.array(xi) for xi in src])
    df_src = pd.DataFrame(data=data_src[1:, 0:], columns=data_src[0, 0:])

    print(df_tar.to_string())
    print(df_src.to_string())

    schema_tar = list(df_tar.columns.values)
    schema_src = list(df_src.columns.values)

    print(schema_tar)
    print(schema_src)

    src_values = []
    tar_values = []
    src_val_len = 0
    tar_val_len = 0
    for attr in schema_src:
        src_values.extend(list(df_src[attr]))
        src_val_len = len(list(df_src[attr]))

    for attr in schema_tar:
        tar_values.extend(list(df_tar[attr]))
        tar_val_len = len(list(df_tar[attr]))

    from similarity.ngram import NGram
    twogram = NGram(2)

    match_threshold = 0.6
    sim_matrix = np.zeros((len(schema_src), len(schema_tar)))

    for i in range(len(src_values)):
        src_value = src_values[i]
        src_ind = i // src_val_len
        src_attr = schema_src[src_ind]

        for j in range(len(tar_values)):
            tar_value = tar_values[j]
            tar_ind = j // tar_val_len
            tar_attr = schema_tar[tar_ind]

            sim_score = 1 - twogram.distance(str(src_value), str(tar_value))

            if str(src_value) == 'None' or str(tar_value) == 'None':
                sim_score = 0

            if sim_score > match_threshold:
                sim_matrix[src_ind, tar_ind] += sim_score
                print('sim_score >= ', match_threshold, ': ', src_attr, tar_attr, src_value, tar_value, sim_score)

    df_sim_matrix = pd.DataFrame(data=sim_matrix, columns=schema_tar, index=schema_src)
    print(df_sim_matrix.to_string())

def test_groupby():
    import numpy as np
    import pandas as pd
    import pprint
    tar = [['attr1', 'attr2', 'attr3'], ['aaaa', 'bbb', 'ccc'], ['aaaa', 'yyyy', 'zzz'], ['xxx', 'bbb', 'zzz'], ['xxx', str(None), str(None)]]

    data_tar = np.array([np.array(xi) for xi in tar])
    df_tar = pd.DataFrame(data=data_tar[1:, 0:], columns=data_tar[0, 0:])
    print(df_tar.to_string())

    schema_tar = list(df_tar.columns.values)
    kb = {}
    for attr in schema_tar:
        kb[attr] = {}
        groups = df_tar.groupby([attr])[attr]
        print(list(groups.groups.keys()))
        for key, item in groups:
            # print(attr, key, groups.get_group(key).values)
            # print('attr:%s val:%s count:%d' % (attr, key, len(groups.get_group(key).values)))
            kb[attr][key] = len(groups.get_group(key).values)

    pprint.pprint(kb)

def test_compare_datatypes_and_del_cols():
    import build_graphical_model as bgm
    import pandas as pd
    import json
    datasets_path = '../thesis_project_dataset_clean/'
    datasource = 'important trees'
    tar_df = pd.read_csv(datasets_path + datasource + '.csv', index_col=0, header=0)
    schema_f = open('../schema_complete_list.json', 'r')
    schema_set = json.load(schema_f, strict=False)

    tar_df = bgm.df_rename_cols(tar_df)
    tar_schema = list(tar_df.columns.values)

    src_datatype = 'esriFieldTypeString'
    attr_schema = schema_set[datasource]
    cols_to_delete = bgm.compare_datatypes(src_datatype, attr_schema, tar_schema)
    tar_df = bgm.df_delete_cols(tar_df, cols_to_delete)
    print(tar_df.head())

def test_form_new_clusters():

    import pprint
    import pandas as pd
    import numpy as np
    import scipy.cluster.hierarchy as hac
    import scipy.spatial.distance as ssd
    import scipy


    def find_all_subtree_mappings(root):
        '''
        For comparing clusters:
        Extract mappings first, represent in vectors, then perform clustering for mappings
        Split topic into two if two distinct clusters are found within topic, can split into more
        Merge clusters into one topic if two clusters from two topics have similar mappings
        '''
        mappings = []
        # mapping_pairs = {}

        for concept in root:
            for dataset in root[concept]:
                if 'cluster' not in root[concept][dataset]:
                    continue
                for mapped_dataset in root[concept][dataset]['cluster']:
                    mapping = [concept,
                                 dataset,
                                 mapped_dataset,
                                 root[concept][dataset]['attribute'],
                                 root[concept][dataset]['cluster'][mapped_dataset]['attribute'],
                                 root[concept][dataset]['cluster'][mapped_dataset]['match_score']]
                    mappings.append(mapping)

                    fwd_attrs = dataset+'AND'+mapped_dataset
                    bkwd_attrs = mapped_dataset+'AND'+dataset
                    # if fwd_attrs in mapping_pairs:
                    #     mapping_pairs[fwd_attrs] += 1
                    # elif bkwd_attrs in mapping_pairs:
                    #     mapping_pairs[bkwd_attrs] += 1
                    # else:
                    #     mapping_pairs[fwd_attrs] = 0

        # pprint.pprint(mappings)

        return mappings

    def hierarchical_cluster_linkage(features, decision_threshold):

        arr = scipy.array(features)
        pd = ssd.pdist(arr, metric='cosine')
        z = hac.linkage(pd)

        pprint.pprint(pd)

        part = hac.fcluster(z, decision_threshold, 'distance')
        return part

    def hierarchical_cluster(scores, a_keys):
        decision_threshold = 0.5

        if len(scores) < 2:
            return []

        a_len = len(a_keys)
        # a = [a[key] for key in a_keys]
        a = np.zeros(shape=(a_len, a_len))

        k = 0
        for i in range(a_len):
            for j in range(i + 1, a_len):
                a[i, j] = scores[k]
                a[j, i] = scores[k]
                # print(a[i, j], a[j, i])
                k += 1

        # a = np.array([[0, 0, 2, 2],
        #               [0, 0, 2, 2],
        #               [2, 2, 0, 0],
        #               [2, 2, 0, 0]])

        a = ssd.squareform(a)
        print(a)

        z = hac.linkage(a)

        part = hac.fcluster(z, decision_threshold, 'inconsistent')
        # print(part)

        # for cluster in set(part):
        #     print(cluster)

        return part


    # need to know all concepts in root so far
    # do N! comparisons of mappings
    def split_concepts(root, mappings):
        '''split to a new temp concept'''

        decision_threshold = 0.5
        mappings = pd.DataFrame(mappings, columns=['concept', 'src_dataset', 'tar_dataset', 'src_attr', 'tar_attr', 'score'])
        concepts = list(root.keys())

        # print(concepts)

        for concept in concepts:
            # filter mappings for the concept
            # concept_mappings = [tuple for tuple in mappings if tuple[0] == concept]
            concept_mappings = mappings.loc[mappings['concept'] == concept]
            print(concept_mappings)

            clusters = concept_mappings.groupby(['src_dataset', 'src_attr'])
            keys = list(clusters.groups.keys())
            num_keys = len(keys)

            clusters_to_split = {}
            clusters_to_split_list = []
            for i in range(num_keys):
                key_i = keys[i]
                cluster_i = clusters.get_group(key_i)

                list_i = []
                for index, row in cluster_i.iterrows():
                    val = row['tar_dataset'] + '.' + row['tar_attr']
                    list_i.append(val)
                num_i = len(list_i)

                for j in range(i+1, num_keys):
                    key_j = keys[j]
                    cluster_j = clusters.get_group(key_j)

                    list_j = []
                    for index, row in cluster_j.iterrows():
                        val = row['tar_dataset'] + '.' + row['tar_attr']
                        list_j.append(val)
                    num_j = len(list_j)

                    diff = set(list_i).symmetric_difference(set(list_j))

                    diff_score = len(list(diff))/(num_i+num_j)
                    # print(diff)
                    diff_score = diff_score if diff_score > decision_threshold else 0
                    if (key_i, key_j) in clusters_to_split:
                    #     clusters_to_split[(key_i, key_j)] += diff_score
                    # elif (key_j, key_i) in clusters_to_split:
                    #     clusters_to_split[(key_j, key_i)] += diff_score
                        pass
                    else:
                        clusters_to_split[(key_i, key_j)] = diff_score
                        clusters_to_split_list.append(diff_score)
                        # print(key_i, key_j)

            # pprint.pprint(clusters_to_split)
            part = hierarchical_cluster(clusters_to_split_list, keys)
            print(part, keys)

            # find clusters to split, then split to new concept
            if len(part) > 1 and len(list(set(part))) > 1:
                num_new_concepts = len(list(set(part))) - 1
                new_concepts = {'temp_'+concept+'_'+str(i+2) : {} for i in range(num_new_concepts)}
                print(new_concepts)

                for j in range(len(keys)):
                    key = keys[j]
                    partition = part[j]
                    if partition != 1:
                        print('temp_'+concept+'_'+str(partition))
                        new_concepts['temp_'+concept+'_'+str(partition)][key[0]] = root[concept][key[0]]
                        del root[concept][key[0]]

                root.update(new_concepts)

        return root




    def merge_concepts(root, mappings):
        '''merge concepts; rename temp concepts not merged this iteration'''
        # merge clusters from different concepts, (or move cluster from first concept to second concept)
        # must also add parent attr to keys, form cluster of attributes
        # when instance matching, compare all values in merged cluster
        # TODO update concept-attr match score, update temp_concept names

        # pprint.pprint(mappings)
        decision_threshold = 0.1
        mappings = pd.DataFrame(mappings, columns=['concept', 'src_dataset', 'tar_dataset', 'src_attr', 'tar_attr', 'score'])
        concepts = list(root.keys())

        clusters = mappings.groupby(['concept', 'src_dataset', 'src_attr'])
        keys = list(clusters.groups.keys())
        num_keys = len(keys)
        # print(num_keys)

        # all clusters must share one edge with each other
        # number of attrs shared must be at least decision_threshold to be considered for merging
        # decide which cluster to merge into

        # key is sorted tuple of datasource.attr
        clusters_to_merge = {}
        features = []
        features_row_keys = []

        # collect all attrs in mappings as cols in matrix
        all_attrs = []
        for i in range(num_keys):
            key_i = keys[i]
            cluster_i = clusters.get_group(key_i)
            all_attrs.append(key_i[1] + 'DOT' + key_i[2])

            for index, row in cluster_i.iterrows():
                val = row['tar_dataset'] + 'DOT' + row['tar_attr']
                all_attrs.append(val)

        # print(all_attrs)
        all_attrs = list(set(all_attrs))
        all_attrs.sort()
        all_attrs_keys = {}
        all_attrs_len = len(all_attrs)
        for i in range(all_attrs_len):
            all_attrs_keys[all_attrs[i]] = i
        # print(all_attrs_keys)
        len_keys = len(all_attrs_keys.keys())
        # print(len_keys)

        for i in range(num_keys):
            key_i = keys[i]
            cluster_i = clusters.get_group(key_i)

            feature_vec = [0] * len_keys

            # attr with concept also included
            index = all_attrs_keys[key_i[1] + 'DOT' + key_i[2]]
            feature_vec[index] = 1

            for index, row in cluster_i.iterrows():
                index = all_attrs_keys[row['tar_dataset'] + 'DOT' + row['tar_attr']]
                feature_vec[index] = 1

            features.append(feature_vec)
            features_row_keys.append((key_i[0], key_i[1], key_i[2]))

        pprint.pprint(features)

        part = hierarchical_cluster_linkage(features, decision_threshold)
        pprint.pprint(part)

        # features_df = pd.DataFrame(features, index=features_row_keys, columns=all_attrs)
        # print(features_df.to_string())

        if len(part) <= 1 or len(list(set(part))) <= 1:
            return root

        part_indexes = [[part[i], i] for i in range(len(part))]
        part_indexes_df = pd.DataFrame(part_indexes, columns=['group', 'index'])
        # print(part_indexes_df.to_string())

        groups_df = part_indexes_df.groupby('group')['index'].apply(list)
        # print(groups_df.to_string())

        for column in groups_df:
            # print(column)
            if len(column) > 1:
                concept_name = ''
                temp_concept_subtrees = {'temp':{}}
                for i in column:
                    concept = features_row_keys[i][0]
                    if 'temp' not in concept:
                        concept_name = concept_name + '+' + concept

                    temp_concept_subtrees['temp'][features_row_keys[i][1]] = root[concept][features_row_keys[i][1]]
                    del root[concept][features_row_keys[i][1]]

                root[concept_name] = temp_concept_subtrees['temp']


        return root

    # matches = {'important trees': {'match_score': 0.58, 'attribute': 'tree species'}, 'park screen trees': {'cluster': {'park specimen trees': {'match_score': 6506, 'attribute': 'tree species'}}, 'match_score': 0.58, 'attribute': 'tree species'}, 'park specimen trees': {'match_score': 0.8, 'attribute': 'tree'}}
    # root = {'trees': matches}

    # TODO change key to datasource.attr b/c there might be multiple probabilistic mappings per datasource
    matches1 = {'ds1': {'match_score': 0.6, 'attribute': 'attr1',
                       'cluster': {'ds3': {'match_score': 1000, 'attribute': 'attr1'}}},
               'ds2': {'match_score': 0.6, 'attribute': 'attr1',
                       'cluster': {'ds3': {'match_score': 1000, 'attribute': 'attr1'}}},
               'ds3': {'match_score': 0.8, 'attribute': 'attr2',
                       'cluster': {'ds1': {'match_score': 2000, 'attribute': 'attr3'},
                                   'ds2': {'match_score': 3000, 'attribute': 'attr4'}
                                   }}
               }
    matches2 = {'ds2': {'match_score': 0.9, 'attribute': 'attr4',
                       'cluster': {'ds3': {'match_score': 3000, 'attribute': 'attr2'},
                                   'ds1': {'match_score': 1800, 'attribute': 'attr3'}
                                   }}
                }
    root = {'c1': matches1, 'c2': matches2}



    # split or merge clusters
    mappings_all = find_all_subtree_mappings(root)
    # pprint.pprint(mappings_all)

    root = split_concepts(root, mappings_all)
    # pprint.pprint(root)

    mappings_all = find_all_subtree_mappings(root)
    # pprint.pprint(mappings_all)

    print('=====')
    root = merge_concepts(root, mappings_all)
    # pprint.pprint(root)
    print('=====')

    return root



def test_find_new_concepts(root):
    import json
    import pprint

    def traverse_tree_for_attrs(root, datasource):
        '''For finding new concepts'''
        mappings = []

        for concept in root:
            # print(concept)
            for dataset in root[concept]:

                # print(dataset)
                dataset_attr = root[concept][dataset]['attribute']
                dataset_attr_score = root[concept][dataset]['match_score']
                if dataset == datasource:
                    mappings.append((concept, dataset_attr, dataset_attr_score))

                if 'cluster' not in root[concept][dataset]:
                    continue
                for mapped_dataset in root[concept][dataset]['cluster']:
                    mapped_dataset_attr = root[concept][dataset]['cluster'][mapped_dataset]['attribute']
                    mapped_dataset_attr_score = root[concept][dataset]['cluster'][mapped_dataset]['match_score']

                    if mapped_dataset == datasource:
                        mappings.append((concept, mapped_dataset_attr, mapped_dataset_attr_score))
        return mappings

    # open output from previous stage
    schema_f = open('../schema_complete_list.json', 'r')
    schema_set = json.load(schema_f, strict=False)
    datasources = ['important trees', 'park specimen trees', 'park screen trees']
    attr_schema = [schema_set[datasource] for datasource in datasources]

    # add new concepts
    attr_schema_parse = {datasource: [] for datasource in datasources}
    for datasource, schema in zip(datasources, attr_schema):
        for attr in schema:
            name = attr['name']
            attr_schema_parse[datasource].append(name)

    # pprint.pprint(attr_schema_parse)
    # TODO toy example for schema

    attr_schema_parse = {'ds1': ['attr1','attr2','attr3'],
                         'ds2': ['attr1','attr2','attr3','attr4'],
                         'ds3': ['attr1','attr2','attr3','attr4']}

    new_concepts = {}

    for ds in list(attr_schema_parse.keys()):
        mappings_datasource = traverse_tree_for_attrs(root, ds)
        # print(ds)
        # pprint.pprint(mappings_datasource)

        attrs = []
        for mapping in mappings_datasource:
            attrs.append(mapping[1])

        attrs = list(set(attrs))
        # print(attrs)

        # find attrs not in map
        diff = set(attr_schema_parse[ds]).symmetric_difference(set(attrs))
        diff = list(diff)
        # print(diff)

        for new_attr in diff:
            if new_attr in new_concepts:
                new_concepts[new_attr].append(ds)
            else:
                new_concepts[new_attr] = [ds]

    # TODO only select some of these attrs as new concepts in next iteration
    print(new_concepts)
    return new_concepts


def test_hierarchical_cluster_linkage():
    import scipy
    import scipy.cluster.hierarchy as hac
    import scipy.spatial.distance as ssd

    arr = scipy.array([[0, 5], [1, 5], [-1, 5], [0, -5], [1, -5], [-1, -5], [-1.1, -5]])
    pd = ssd.pdist(arr)
    dm = ssd.squareform(pd)
    res1 = hac.linkage(pd)
    res2 = hac.linkage(dm)
    res3 = hac.linkage(arr)

    # print(res1)
    # print(res2)
    # print(dm)
    # print(res3)

    part = hac.fcluster(res3, 0.5, 'inconsistent')
    print(part)

    return


root = test_form_new_clusters()
test_find_new_concepts(root)