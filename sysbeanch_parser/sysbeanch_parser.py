import optparse
import re
import json

def remove_units(key_value,unit):
    measures = ['time','size']
    if(key_value and unit in key_value[1]):
        for m in measures:
            if(m in key_value[0]):
                key_value[0]+='_('+unit+')'
                key_value[1] = key_value[1].replace(unit, '')   
                return key_value
    return key_value

def remove_non_numeric(key_value):
    key_value = remove_units(key_value,'KiB')
    key_value = remove_units(key_value,'MiB')
    key_value = remove_units(key_value,'s') 
    return key_value


def remove_stdev_avg(key_value):
    new_new_dictionary = {}
    top_key = ''
    if('(avg/stddev)' in key_value[0]):
        top_key = re.findall(r'.+_\(', key_value[0])[0]
        avg_stdev_key = key_value[0].replace(top_key, '').replace(')', '').split('/')
        top_key = top_key[:-2]
        avg_stdev_val =  key_value[1].split('/')
        new_new_dictionary = {}
        new_new_dictionary[avg_stdev_key[0]] = avg_stdev_val[0]
        new_new_dictionary[avg_stdev_key[1]] = avg_stdev_val[1]  
    return new_new_dictionary,top_key


def remove_persecond(key_value):
    new_new_dictionary = {}
    top_key = ''
    if('persecond)' in key_value[1]):
        top_key = key_value[0]
        values = key_value[1].split('(')
        values[1] = values[1].replace('persecond)', '')
        new_new_dictionary = {}
        new_new_dictionary['num'] = values[0]
        new_new_dictionary['per_second'] = values[1] 
    return new_new_dictionary,top_key

def parse_sysbeanch(sysbeanch_file):
    report_dictionary = {}
    new_dictionary = None
    for line in sysbeanch_file:
        if ':' in line and not 'WARNING' in line:
            line = line.strip()
            key_value = line.split(':')
            key_value[0] = key_value[0].replace(' ', '_')
            key_value[1] = key_value[1].replace(' ', '')
            if (not key_value[1]):
                new_dictionary = {}
                prev_key = key_value[0]
            if(key_value[1]):
                key_value = remove_non_numeric(key_value)    
                new_new_dictionary,top_key = remove_stdev_avg(key_value)
                if(new_new_dictionary):
                    new_dictionary[top_key] = new_new_dictionary
                    continue
                new_new_dictionary,top_key = remove_persecond(key_value)
                if(new_new_dictionary):
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
    