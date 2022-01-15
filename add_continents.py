# Annie Kuo

# IMPORT MODULE
import doctest


# DEFINE FUNCTIONS
def get_iso_codes_by_continent(filename):
    """ (str) -> dict

    The function takes as input a string representing a filename.
    The function returns a dictionary mapping continents' names to
    a list of ISO codes of countries that belong to that continent.
    
    >>> d = get_iso_codes_by_continent("iso_codes_by_continent.tsv")
    >>> len(d['ASIA'])
    50
    >>> len(d['NORTH AMERICA'])
    23
    >>> d['AFRICA'][2]
    'NAM'
    >>> d['EUROPE'][10]
    'MDA'
    >>> len(d)
    6
    
    >>> fobj = open("test1.txt", "w", encoding= "UTF-8")
    >>> strings = ["BLR\\tEurope"]
    >>> strings.append("MLT\\tEurope")
    >>> fobj.write("\\n".join(strings))
    21
    >>> fobj.close()
    >>> d = get_iso_codes_by_continent("test1.txt")
    >>> len(d['EUROPE'])
    2
    >>> d['EUROPE'][0]
    'BLR'
    >>> d['EUROPE'][1]
    'MLT'
    
    >>> fobj = open("test2.txt", "w", encoding= "UTF-8")
    >>> strings = ["GMB\\tAfrica"]
    >>> strings.append("MLT\\tEurope")
    >>> strings.append("ERI\\tAfrica")
    >>> fobj.write("\\n".join(strings))
    32
    >>> fobj.close()
    >>> d = get_iso_codes_by_continent("test2.txt")
    >>> len(d['EUROPE'])
    1
    >>> len(d['AFRICA'])
    2
    """
    # initialize variable
    continents = {}
    
    # read the file
    fobj= open(filename, "r", encoding= "UTF-8")
    
    # isolate the information in each line
    for line in fobj:
        data = line.split("\t")
        continent = data[1].upper()
        continent = continent.strip("\n")
        
        # in case there is no key with that continent
        if continent not in continents:
            continents[continent] = [data[0]]
        # in case the is already a key with that continent
        else:
            continents[continent].append(data[0])
        
    fobj.close()
    
    # return the dictionary
    return continents


def add_continents_to_data(input_filename, continents_filename, output_filename):
    """ (str, str, str) -> int
    
    The function takes as input three strings representing file names.
    It reads the input_filename, adds the continent of the corresponding countries and
    write the new version to ouput_filename.
    The function returns an integer indicating the number of lines written to output_filename.
    
    >>> add_continents_to_data("small_clean_co2_data.tsv", "iso_codes_by_continent.tsv", "small_co2_data.tsv")
    10
    
    >>> fobj = open("continent_test1.txt", "w", encoding= "UTF-8")
    >>> fobj.write("RUS\\tRussia\\t1971\\t1533.262\\t130831000")
    34
    >>> fobj.close()
    >>> add_continents_to_data("continent_test1.txt", "iso_codes_by_continent.tsv", "continent_test2.tsv")
    1
    >>> fobj = open("continent_test2.tsv", "r", encoding= "UTF-8")
    >>> file_content = fobj.read()
    >>> file_content == "RUS\\tRussia\\tASIA,EUROPE\\t1971\\t1533.262\\t130831000"
    True
    >>> fobj.close()
    
    >>> fobj = open("continent_test3.txt", "w", encoding= "UTF-8")
    >>> fobj.write('TUR\\tTurkey\\t1900\\t1.037\\t14030306')
    30
    >>> fobj.close()
    >>> add_continents_to_data("continent_test3.txt", "iso_codes_by_continent.tsv", "continent_test4.tsv")
    1
    >>> fobj = open("continent_test4.tsv", "r", encoding= "UTF-8")
    >>> file_content = fobj.read()
    >>> file_content == "TUR\\tTurkey\\tASIA,EUROPE\\t1900\\t1.037\\t14030306"
    True
    >>> fobj.close()
    """
    # initialize variables
    num_of_lines = 0
    new_lines = []
    
    # retrieve a dictionary of countries per continent
    countries_per_continent = get_iso_codes_by_continent(continents_filename)
    
    # read the input_filename
    fobj= open(input_filename, "r", encoding= "UTF-8")
    
    # create a list of all the lines
    for line in fobj:
        new_lines.append(line)
        
    # modify the lines according to their continent
    for index in range(len(new_lines)):
        line = new_lines[index]
        columns = line.split("\t")
        
        # find its continent(s)
        iso_code = columns[0]
        line_continent = []
        
        for continent in countries_per_continent:
            if iso_code in countries_per_continent[continent]:
                line_continent.append(continent)
        
        # add the continent(s) to the line of data
        columns[2:2] = [",".join(line_continent)]
        new_lines[index] = "\t".join(columns)
        
    fobj.close()
    
    # write the new output_filename
    fobj= open(output_filename, "w", encoding= "UTF-8")
    for line in new_lines:
        fobj.write(line)
        num_of_lines += 1
    fobj.close()
    
    # return the number of lines
    return num_of_lines    
    


# TEST MODULE
if __name__ == "__main__":
    doctest.testmod()