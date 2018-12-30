import optparse
import re
import json

def parse_sysbeanch(sysbeanch_file):
    report_dictionary = {}
    new_dictionary = None
    for line in sysbeanch_file:
        if ':' in line:
            line = line.strip()
            key_value = line.split(':')
            key_value[0] = key_value[0].replace(' ', '_')
            key_value[1] = key_value[1].replace(' ', '')
#            print(key_value)
            if (not key_value[1]):
                new_dictionary = {}
                prev_key = key_value[0]
            if(key_value[1]):
                if('s' in key_value[1]):
                    key_value[0]+="_(s)"
                    key_value[1] = key_value[1].replace('s', '')
                if('(avg/stddev)' in key_value[0]):
                    top_key = re.findall(r'.+_\(', key_value[0])[0]
                    avg_stdev_key = key_value[0].replace(top_key, '').replace(')', '').split('/')
                    top_key = top_key[:-2]
                    avg_stdev_val =  key_value[1].split('/')
                    new_new_dictionary = {}
                    new_new_dictionary[avg_stdev_key[0]] = avg_stdev_val[0]
                    new_new_dictionary[avg_stdev_key[1]] = avg_stdev_val[1]
                    new_dictionary[top_key] = new_new_dictionary
                    continue
                new_dictionary[key_value[0]] = key_value[1]
            report_dictionary[prev_key] = new_dictionary
    return report_dictionary

if __name__ == "__main__":
    parser = optparse.OptionParser()
    
    parser.add_option('-s', '--sysbeanch_report', action="store", dest="sysbeanch_report", help="The sysbench report as a file")
    
    
    options, args = parser.parse_args()
    
    f = open(options.sysbeanch_report, "r")
    report_dictionary = parse_sysbeanch(f)
    print(json.dumps(report_dictionary))
    