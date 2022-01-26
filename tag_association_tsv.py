#!/usr/bin/env python3
import tag_analysis as ta
import argparse


def main():
    parser = argparse.ArgumentParser(description='A script that returns a tsv file of the frequency of all the tags associated with a tag')
    parser.add_argument('-path', '-t_path', '-tagsTSV_path', type=str, dest='tagsTSV_path', help='Specify the path to the tags.tsv adn tags_obj.tsv file (the file with all the tags number and names)')
    parser.add_argument('-t', '-tag_name', dest='tag', nargs='?', type=str,  help='Put this at the end of the script and type the tag name.')
    parser.add_argument('-o', '-o', dest='output', type=str, help='Type the outputs path for the tsv file')
    results = parser.parse_args()
    
    if results.tag is None:
        raise ValueError("!!Please enter a tag name!!")
    if results.tagsTSV_path is None:
        raise ValueError("!!Please enter the path to the tsv files!!")

    key = results.tag.replace(" ",'').lower()
    if results.output is None:
        ta.tag_association_tsv_print(results.tagsTSV_path, key)
    else:
        ta.tag_association_tsv(results.tagsTSV_path, key, results.output)


if __name__ == '__main__':
    main()