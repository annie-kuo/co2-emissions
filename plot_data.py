# Annie Kuo

# IMPORT MODULES
import doctest
import matplotlib.pyplot as plt
from data_cleanup import *
from add_continents import *
from build_countries import *



# DEFINE HELPER FUNCTIONS
def shorten_names(all_continents):
    """ (list) -> NoneType
    
    The function shortens the names of continents whose name is long
    ie. NORTH AMERICA and SOUTH AMERICA
    
    >>> a = ['ASIA', 'AFRICA', 'EUROPE', 'SOUTH AMERICA']
    >>> shorten_names(a)
    >>> a
    ['ASIA', 'AFRICA', 'EUROPE', 'S. AMERICA']
    
    >>> b = ['NORTH AMERICA', 'AFRICA', 'SOUTH AMERICA']
    >>> shorten_names(b)
    >>> b
    ['N. AMERICA', 'AFRICA', 'S. AMERICA']
    
    >>> c = ['EUROPE', 'AFRICA', 'ASIA', 'OCEANIA']
    >>> shorten_names(c)
    >>> c
    ['EUROPE', 'AFRICA', 'ASIA', 'OCEANIA']
    """
    for index in range(len(all_continents)):
        if all_continents[index] == "SOUTH AMERICA":
            all_continents[index] = "S. AMERICA"
        elif all_continents[index] == "NORTH AMERICA":
            all_continents[index] = "N. AMERICA"



# DEFINE FUNCTIONS
def get_bar_co2_pc_by_continent(dict_by_iso_codes, year):
    """ (dict, int) -> list
    
    The function creates a bar plot representing the co2 emissions per capital
    (in tonnes) produced by all countries in each continent.
    It returns a list of the values being plotted.
    
    >>> d1 = get_countries_from_file("small_co2_data.tsv")
    >>> get_bar_co2_pc_by_continent(d1, 2001)
    [0.20320332558992543, 67.01626016260163, 7.6609004739336495, 1.4196063588190764]
    
    >>> reset = plt.figure()
    >>> d2 = get_countries_from_file("large_co2_data.tsv")
    >>> data = get_bar_co2_pc_by_continent(d2, 1994)
    >>> len(data)
    6
    >>> round(data[0], 5) # AFRICA
    1.03062
    >>> round(data[1],5) # ASIA
    2.63988
    
    >>> reset = plt.figure()
    >>> d3 = get_countries_from_file("small_co2_data.tsv")
    >>> data = get_bar_co2_pc_by_continent(d3, 2001)
    >>> len(data)
    4
    >>> round(data[2], 5) # EUROPE
    7.6609
    >>> round(data[3],5) # S. AMERICA
    1.41961
    """
    # initialize variables
    all_countries = []
    co2_emissions = []
    
    # compile all Country objects
    for iso_code in dict_by_iso_codes:
        country = dict_by_iso_codes[iso_code]
        all_countries.append(country)
    
    # sort the Country objects by their continent
    countries_per_continent = Country.get_countries_by_continent(all_countries)
    
    # create a list of all continents from the dictionary's keys
    all_continents = list(countries_per_continent.keys())
    all_continents.sort()
    
    # compute the continent's co2 emission per capita for the given year
    for continent in all_continents:
        countries = countries_per_continent[continent]
        continent_co2_emission = Country.get_total_co2_emissions_per_capita_by_year(countries, year)
        co2_emissions.append(continent_co2_emission)
    
    # shorten names of continents
    shorten_names(all_continents)
            
    # plot the data
    plt.bar(all_continents, co2_emissions)
    
    # define the graph's properties
    title = "CO2 emissions per capita in " + str(year) + " by annie.kuo@mail.mcgill.ca"
    plt.title(title)
    plt.ylabel("co2 (in tonnes)")
    
    # save the graph
    fig_name = "co2_pc_by_continent_" + str(year) + ".png"
    plt.savefig(fig_name)

    # return a list of the values plotted
    return co2_emissions


def get_bar_historical_co2_by_continent(dict_by_iso_codes, year):
    """ (dict, int) -> list
    
    The function creates a bar plot representing the historical co2 emissions (in
    millions of tonnes) produced by all countries in each continent.
    It returns a list of the values being plotted.
    
    >>> reset = plt.figure()
    >>> d1 = get_countries_from_file("small_co2_data.tsv")
    >>> get_bar_historical_co2_by_continent(d1, 2015)
    [4.877, 207.54500000000002, 359.367, 149.34300000000002]
    
    >>> reset = plt.figure()
    >>> d2 = get_countries_from_file("large_co2_data.tsv")
    >>> data = get_bar_historical_co2_by_continent(d2, 2020)
    >>> len(data)
    6
    >>> round(data[2], 5) # EUROPE
    523681.833
    >>> round(data[4], 5) # OCEANIA
    19845.01
    
    >>> reset = plt.figure()
    >>> d2 = get_countries_from_file("small_co2_data.tsv")
    >>> data = get_bar_historical_co2_by_continent(d2, 2001)
    >>> len(data)
    4
    >>> round(data[1], 5) # ASIA
    41.215
    >>> round(data[2], 5) # EUROPE
    355.619
    """
    # initialize variables
    all_countries = []
    co2_emissions = []
    
    # compile all Country objects
    for iso_code in dict_by_iso_codes:
        country = dict_by_iso_codes[iso_code]
        all_countries.append(country)
    
    # sort the Country objects by their continent
    countries_per_continent = Country.get_countries_by_continent(all_countries)
    
    # create a list of all continents from the dictionary's keys
    all_continents = list(countries_per_continent.keys())
    all_continents.sort()
    
    # compute the continent's historic co2 emission up until the given year
    for continent in all_continents:
        countries = countries_per_continent[continent]
        continent_co2_emission = Country.get_total_historical_co2_emissions(countries, year)
        co2_emissions.append(continent_co2_emission)
    
    # shorten names of continents
    shorten_names(all_continents)
            
    # plot the data
    plt.bar(all_continents, co2_emissions)
    
    # define the graph's properties
    title = "Historical CO2 emissions up to " + str(year) + " by annie.kuo@mail.mcgill.ca"
    plt.title(title)
    plt.ylabel("co2 (in millions of tonnes)")
    
    # save the graph
    fig_name = "hist_co2_by_continent_" + str(year) + ".png"
    plt.savefig(fig_name)

    # return a list of the values plotted
    return co2_emissions


def get_bar_co2_pc_top_ten(dict_by_iso_codes, year):
    """ (dict, int) -> list
    
    The function creates a bar plot representing the co2 emissions per capital
    (in tonnes) produced by the top 10 producing countries in the dictionary.
    It returns a list of the values being plotted.
    
    >>> reset = plt.figure()
    >>> d1 = get_countries_from_file("small_co2_data.tsv")
    >>> data = get_bar_co2_pc_top_ten(d1, 2001)
    >>> len(data)
    5
    >>> round(data[0], 5)
    67.01626
    >>> round(data[4], 4)
    0.2032
    
    >>> reset = plt.figure()
    >>> d2 = get_countries_from_file("large_co2_data.tsv")
    >>> data = get_bar_co2_pc_top_ten(d2, 1994)
    >>> len(data)
    10
    >>> round(data[0], 5) # QAT
    60.56016
    >>> round(data[1], 5) # KWT
    33.28873
    >>> round(data[2], 5) # ARE
    31.64996
    
    >>> reset = plt.figure()
    >>> d3 = get_countries_from_file("small_co2_data.tsv")
    >>> data = get_bar_co2_pc_top_ten(d3, 2002)
    >>> len(data)
    1
    >>> round(data[0], 5)
    1.19898
    """
    # initialize variables
    co2_emission_by_country = {}
    top_ten_iso_codes = []
    top_ten_co2_emissions = []
    
    # generate a dictionary mapping Country objects to their co2 emission per capital
    for iso_code in dict_by_iso_codes:
        country = dict_by_iso_codes[iso_code]
        co2_emission = country.get_co2_per_capita_by_year(year)
        # add to dictionary only if the data is available
        if co2_emission != None:
            co2_emission_by_country[country] = co2_emission
    
    # sort which data to be plotted
    top_ten = Country.get_top_n(co2_emission_by_country, 10)
    
    # separate data according to the axis
    for iso_code, co2_emission in top_ten:
        top_ten_iso_codes.append(iso_code)
        top_ten_co2_emissions.append(co2_emission)

    # plot the data
    plt.bar(top_ten_iso_codes, top_ten_co2_emissions)
    
    # define the graph's properties
    title = "Top 10 countries for CO2 emissions pc in " + str(year) + " by annie.kuo@mail.mcgill.ca"
    plt.title(title)
    plt.ylabel("co2 (in tonnes)")
    
    # save the graph
    fig_name = "top_10_co2_pc_" + str(year) + ".png"
    plt.savefig(fig_name)

    # return a list of the values plotted
    return top_ten_co2_emissions


def get_bar_top_ten_historical_co2(dict_by_iso_codes, year):
    """ (dict, int) -> list
    
    The function creates a bar plot representing the historical co2 emissions
    (in millions of tonnes) produced by the top 10 producing countries
    in the dictionary.
    It returns a list of the values being plotted.
    
    >>> reset = plt.figure()
    >>> d1 = get_countries_from_file("small_co2_data.tsv")
    >>> get_bar_top_ten_historical_co2(d1, 2015)
    [306.696, 166.33, 149.34300000000002, 48.923, 41.215, 3.748, 3.324, 1.553, 0.0]
    >>> d2 = get_countries_from_file("large_co2_data.tsv")
    >>> data = get_bar_top_ten_historical_co2(d2, 2018)
    >>> len(data)
    10
    >>> data[0] # USA
    404769.39699999994
    >>> data[1] # CHN
    210201.179
    >>> data[8] # CAN
    32517.775000000034
    
    >>> reset = plt.figure()
    >>> d2 = get_countries_from_file("large_co2_data.tsv")
    >>> data = get_bar_top_ten_historical_co2(d2, 1900)
    >>> len(data)
    10
    >>> round(data[0], 5) # GBR
    16734.16
    >>> round(data[3], 5) # FRA
    3710.464
    >>> round(data[5], 5) # POL
    1335.35
    
    >>> reset = plt.figure()
    >>> d2 = get_countries_from_file("small_co2_data.tsv")
    >>> data = get_bar_top_ten_historical_co2(d2, 2019)
    >>> len(data)
    9
    >>> round(data[0], 5) # POL
    306.696
    >>> round(data[1], 5) # PAK
    166.33
    >>> round(data[2], 5) # COL
    149.343
    """
    # initialize variables
    co2_emission_by_country = {}
    top_ten_iso_codes = []
    top_ten_co2_emissions = []
    
    # generate a dictionary mapping Country objects to their historical co2 emission
    for iso_code in dict_by_iso_codes:
        country = dict_by_iso_codes[iso_code]
        co2_emission = country.get_historical_co2(year)
        co2_emission_by_country[country] = co2_emission
    
    # sort which data to be plotted
    top_ten = Country.get_top_n(co2_emission_by_country, 10)
    
    # separate data according to the axis
    for iso_code, co2_emission in top_ten:
        top_ten_iso_codes.append(iso_code)
        top_ten_co2_emissions.append(co2_emission)

    # plot the data
    plt.bar(top_ten_iso_codes, top_ten_co2_emissions)
    
    # define the graph's properties
    title = "Top 10 countries for historical CO2 up to " + str(year) + " by annie.kuo@mail.mcgill.ca"
    plt.title(title)
    plt.ylabel("co2 (in millions of tonnes)")
    
    # save the graph
    fig_name = "top_10_hist_co2_" + str(year) + ".png"
    plt.savefig(fig_name)

    # return a list of the values plotted
    return top_ten_co2_emissions


def get_plot_co2_emissions(dict_by_iso_codes, iso_codes, min_year, max_year):
    """ (dict, list, int, int) -> list
    
    The function plots the co2 emissions of the selected countries from
    min_year to max_year.
    It returns a 2D list for which each sublist contains the co2 emission of
    a selected country from min_year to max_year, and the position of the sublist
    matches the position of the ISO code in the input list.
    
    >>> reset = plt.figure()
    >>> d2 = get_countries_from_file("large_co2_data.tsv")
    >>> data = get_plot_co2_emissions(d2, ["USA", "CHN", "RUS", "DEU", "GBR"], 1990, 2000)
    >>> len(data)
    5
    >>> len(data[1]) # CHN
    11
    >>> data[0][:5] # USA
    [5121.179, 5071.564, 5174.671, 5281.387, 5375.034]

    >>> reset = plt.figure()
    >>> d2 = get_countries_from_file("large_co2_data.tsv")
    >>> data = get_plot_co2_emissions(d2, ["COL", "PAK", "GBR"], 2000, 2020)
    >>> len(data[0]) # COL
    21
    >>> data[2][5] # GBR
    569.7
    >>> data[1][5] # GBR
    134.756
    
    >>> reset = plt.figure()
    >>> d2 = get_countries_from_file("small_co2_data.tsv")
    >>> data = get_plot_co2_emissions(d2, ["COL", "LSO", "CMR"], 1995, 2000)
    >>> len(data[0]) # COL
    6
    >>> data[2][1] # GBR
    0.0
    >>> data[1][1] # GBR
    0.0
    """
    # initialize variables
    styles = [".:b", "s:c", "*:k", "x:m", "D:g"]
    counter = 0
    list_2D = []
    copy_iso_codes = iso_codes[:]
    
    # determine data points to plot
    if (max_year - min_year) > 10:
        increment = (max_year - min_year) // 10
    else:
        increment = 1
    years_to_plot = range(min_year, max_year + 1, increment)
    
    for iso_code in copy_iso_codes:
        # update the 2D list to return
        sublist = []
        if iso_code in dict_by_iso_codes:
            country = dict_by_iso_codes[iso_code]
        # in case there is no data available at all for such country
        # remove country from the list
        else:
            iso_codes.remove(iso_code)
            break
        
        # create and append sublist for that country
        for year in range(min_year, max_year + 1):
            co2_emission = country.get_co2_emissions_by_year(year)
            sublist.append(co2_emission)
        list_2D.append(sublist)
        
        # retrieve and sort the data from the years to plot
        co2_emissions_to_plot = []
        for index in range(0, max_year - min_year + 1, increment):
            co2_emissions_to_plot.append(list_2D[counter][index])
        
        # plot the data
        plt.plot(years_to_plot, co2_emissions_to_plot, styles[counter])
        counter += 1
    
    # define the graph's properties
    title = "CO2 emissions between " + str(min_year) + " and " + str(max_year)
    title += " by annie.kuo@mail.mcgill.ca"
    plt.title(title)
    plt.ylabel("co2 (in millions of tonnes)")
    plt.legend(iso_codes)
    
    # save the graph
    fig_name = "co2_emissions_" + str(min_year) + "_" + str(max_year) + ".png"
    plt.savefig(fig_name)

    # return a list of the values plotted
    return list_2D    



# TEST MODULE
if __name__ == "__main__":
    doctest.testmod()