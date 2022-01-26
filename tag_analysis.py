
import numpy as np
import pandas as pd
import sys

def create_df(tag_obj, tags):
    df_tagsobj = pd.read_csv(tag_obj, sep='\t')
    df_tags = pd.read_csv(tags, sep='\t')

    return df_tagsobj, df_tags

def RandC_filter(df):
    #make sure the tags_obj is a panda df
    #return the courses and resoureces filter
    filter1 = df["tbl"] == "resources"
    filter2 = df["tbl"] == "courses"
    tags_obj = df[filter1 | filter2]

    return tags_obj
def lowercase_nspace_tags(df):
    df['raw_tag_compressed'] = df["raw_tag"].str.lower()
    df['raw_tag_compressed'] = df['raw_tag_compressed'].str.replace(' ','')
    return df

def tags_frequency_df(df):
    #returns the table of the frequency of the tag-id
    freq_tag = df.groupby(['tagid']).count()

    freq_tag = freq_tag.sort_values(by=['tagid'], ascending=True)
    freq_tag = freq_tag.reset_index()[['tagid','objectid']]
    freq_tag.rename(columns={"tagid":"tagid","objectid":"frequency"}, inplace=True)

    return freq_tag

def resource_tags(resource_id, df):
    #returns all the tags associated with resouce or couse
    filter1 = df["objectid"] == resource_id
    resource_ids_df = df[filter1]

    if len(resource_ids_df) == 0:
        sys.exit("This is not a resource or a course")
    else:
        return resource_ids_df

def tag_str2num(tag_str, tags_df):
    try:
        filter1 = tags_df['raw_tag_compressed'] == tag_str
        tagid = tags_df[filter1]
        return tagid.iloc[0]['id']
    except IndexError:
        sys.exit('!!Please enter a valid tag name!!')

    
    
def tag_association(tagid, tangs_obj_df, tags_df):
    #returns all the things associated with a tag
    if isinstance(tagid, (str)) == True:
        tagid = tag_str2num(tagid, tags_df)

    if isinstance(tagid, (int, np.int64)) == True:
        filter2 = tangs_obj_df['tagid'] == tagid
        df = tangs_obj_df[filter2][['tagid', 'objectid']]
        if len(df) == 0:
            #return "!!Please enter a valid tag number!!", False
            sys.exit('!!Please enter a valid tag number!!')
        else:
            return df, tagid


def tag_indexes(tagid, tags_obj_df, tags_df):
    resource_assoc, tagid = tag_association(tagid, tags_obj_df, tags_df)
    df = pd.DataFrame(columns=['tagid','objectid'], dtype=np.int64)
    
    for i in range(len(resource_assoc)):

        x = resource_assoc.iloc[i]['objectid']
        #print(x)
        resource_t = resource_tags(x, tags_obj_df)
        #print(resource_t)
        for j in range(len(resource_t)):
            #print(resource_t.iloc[j]['tagid'])
            if resource_t.iloc[j]['tagid'] != tagid:
                #print(resource_t.iloc[j][['tagid','objectid']])
                df = df.append(resource_t.iloc[j][['tagid','objectid']])
    
    return df

def tag_association_tsv_print(tags_objTSV, tagsTSV, tag, path):
    tags_obj, tags = create_df(tags_objTSV, tagsTSV)
    tags_obj = RandC_filter(tags_obj)
    tags = lowercase_nspace_tags(tags)

    test_num = tag_indexes(tag, tags_obj, tags)

    # if isinstance(test_num, (str)) == True:
    #     print(test_num)
    # else:
    frequencyDF = tags_frequency_df(test_num)
    frequencyDF = frequencyDF.merge(tags, left_on='tagid', right_on="id")[['raw_tag','frequency', 'tagid']].sort_values(['frequency'], ascending=False)
    print(frequencyDF.to_csv(sep="\t", index=False))

def tag_association_tsv(tags_objTSV, tagsTSV, tag, path):
    tags_obj, tags = create_df(tags_objTSV, tagsTSV)
    tags_obj = RandC_filter(tags_obj)
    tags = lowercase_nspace_tags(tags)

    test_num = tag_indexes(tag, tags_obj, tags)

    frequencyDF = tags_frequency_df(test_num)
    frequencyDF = frequencyDF.merge(tags, left_on='tagid', right_on="id")[['raw_tag','frequency', 'tagid']].sort_values(['frequency'], ascending=False)
    frequencyDF.to_csv(path, sep="\t", index=False)

    

def main():

    pass

    #tags_obj, tags = create_df("tags_obj.tsv", "tags.tsv")
    #tags = lowercase_nspace_tags(tags)
    #print(tags)
    #tag_association_tsv_print("tags_obj.tsv", "tags.tsv", "Algorithms")
    
    #x1 = r"C:\Users\Maximilian_Drach_XPS\Desktop\Purdue\Nanohub\Work\tags_obj.tsv"
    #x2 = r"C:\Users\Maximilian_Drach_XPS\Desktop\Purdue\Nanohub\Work\tags.tsv"

    #tag_association_tsv(x1, x2, 1000)

    #df = pd.DataFrame(columns=['tagid','id'], dtype=np.int64)
    #print(tag_association(23717, tags_obj, tags))
    #print(resource_tags(1,tags_obj))
   
    # print(test_num)
    # #testValue = 248
    # #print(tag_association(testValue, tags_obj, tags))
    # #print(resource_tags(1198, tags_obj))
    # #x, xt = tag_association(test_num, tags_obj, tags)
    # #print(len(x))
    # tg=tag_indexes(test_num,tags_obj, tags)
    # test = tags_frequency_df(tg)
    # print(test)
    # #give it a name
    # test.to_csv(r"C:\Users\Maximilian_Drach_XPS\Desktop\Purdue\Nanohub\Work\tag_histogram.tsv", sep="\t")

    


if __name__ == '__main__':
    main()