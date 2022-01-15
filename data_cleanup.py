# Annie Kuo

# IMPORT MODULE
import doctest


# DEFINE FUNCTIONS
def find_delim(string):
    """ (str) -> str

    The function takes a string as input representing a single line of data.
    It returns the most commonly used delimiter in the input string.
    An AssertionError is raised if there are no delimiters in the input.
    
    >>> find_delim("cat\\tdog bat\\tcrab-cod")
    '\\t'
    
    >>> find_delim("1-2-3-4-5")
    '-'
    
    >>> find_delim("hello, how are-you? good.")
    ' '
    
    >>> find_delim("astringwithoutdelimiter")
    Traceback (most recent call last):
    AssertionError
    """
    # initialize variables
    delims = (('\t'), (','), (' '), ('-'))
    delim_counts = []
    
    # count the number of occurences for each delimiter
    for delim in delims:
        count = 0
        # iterate through the input string and update count
        for char in string:
            if char == delim:
                count += 1
        # append the final count to the list of counts
        delim_counts.append(count)
    
    # determine the index of the delimiter with the most counts
    max_count = max(delim_counts)
    
    # raise error if there are no delimiter in the input
    if max_count == 0:
        raise AssertionError
    
    max_index = delim_counts.index(max_count)
    
    # return the delimiter associated with the max count
    return delims[max_index]


def clean_one(input_filename, output_filename):
    """ (str, str) -> int

    The function takes as input two strings: the file name for a file
    to be read, and file name for a file to be written.
    It replaces delimiters in input_filename by a tab
    and write the new version to output_filename.
    The function returns an integer indicating the number of lines written to output_filename.
    
    >>> clean_one('small_raw_co2_data.txt', 'small_tab_sep_co2_data.tsv')
    10
    
    >>> fobj = open("test1.txt", "w", encoding= "UTF-8")
    >>> fobj.write("LSO-Lesotho-1975--1161000")
    25
    >>> fobj.close()
    >>> clean_one('test1.txt', 'first_clean1.txt')
    1

    >>> fobj = open("test2.txt", "w", encoding= "UTF-8")
    >>> strings = ["CMR-Cameroon-2001-3.324-16358000"]
    >>> strings.append("QAT,Qatar,2001,41,215,615000")
    >>> fobj.write("\\n".join(strings))
    61
    >>> fobj.close()
    >>> clean_one('test2.txt', 'first_clean2.txt')
    2
    """
    # initialize variables
    new_lines = []
    num_of_lines = 0
    
    # read the input_filename
    fobj= open(input_filename, "r", encoding= "UTF-8")
    for line in fobj:
        # find the delimiter in the line and replace it with a tab
        delim = find_delim(line)
        new_line = line.replace(delim, "\t")
        # add the modified line to the list of lines to write
        new_lines.append(new_line)
    fobj.close()
    
    # write the new output_filename
    fobj= open(output_filename, "w", encoding= "UTF-8")
    for line in new_lines:
        fobj.write(line)
        num_of_lines += 1
    fobj.close()
    
    # return the number of lines
    return num_of_lines


def final_clean(input_filename, output_filename):
    """ (str, str) -> int

    The function takes as two strings: the file name for a file
    to be read, and file name for a file to be written.
    It modifies each line in input_filename so that it contains exactly 5 columns.
    and writes the modified line into output_filename.
    The function returns an integer indicating the number of lines written to output_filename.
    
    >>> final_clean('small_tab_sep_co2_data.tsv', 'small_clean_co2_data.tsv')
    10
    
    >>> fobj = open("test1.txt", "w", encoding= "UTF-8")
    >>> fobj.write("LSO-Lesotho-1975--1161000")
    25
    >>> fobj.close()
    >>> clean_one('test1.txt', 'first_clean1.txt')
    1
    >>> final_clean('first_clean1.txt', 'final_clean1.tsv')
    1

    >>> fobj = open("test2.txt", "w", encoding= "UTF-8")
    >>> strings = ["CMR-Cameroon-2001-3.324-16358000"]
    >>> strings.append("QAT,Qatar,2001,41,215,615000")
    >>> fobj.write("\\n".join(strings))
    61
    >>> fobj.close()
    >>> clean_one('test2.txt', 'first_clean2.txt')
    2
    >>> final_clean('first_clean2.txt', 'final_clean2.tsv')
    2
    """
    # initialize variables
    new_lines = []
    num_of_lines = 0
    
    # read the input_filename
    fobj= open(input_filename, "r", encoding= "UTF-8")
    
    # create a list of all the lines
    for line in fobj:
        new_lines.append(line)
        
    # modify the lines according to their irregularities  
    for index in range(len(new_lines)):
        line = new_lines[index]
        columns = line.split("\t")
        
        # in case the name is not contained in column 1,
        # the year will not be in column 2
        if not columns[2].isdecimal():
            year_index = 0
            for i in range(len(columns)):
                if columns[i].isdecimal():
                    year_index = i
                    break
            country = " ".join(columns[1 : i])
            columns[1 : i] = [country]
            new_line = "\t".join(columns)
            new_lines[index] = "\t".join(columns)
        
        # in case commas were used to indicate decimals
        # and commas were the delimiters
        if len(columns) == 6 and "." not in line:
            co2_emission = ".".join(columns[3:5])
            columns[3:5] = [co2_emission]
            new_lines[index] = "\t".join(columns)
            
        # in case commas were used to indicate decimals
        # and commas were not the delimiters
        if "," in columns[3]:
            co2_emission = columns[3].replace(",", ".")
            columns[3] = co2_emission
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