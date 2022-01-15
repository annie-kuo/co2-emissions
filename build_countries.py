# Annie Kuo

# IMPORT MODULE
import doctest
import copy

# DEFINE HELPER FUNCTION
def iso_is_valid(code):
    """ (str) -> bool

    The function returns true if the code is a valid iso code, False otherwise.
    
    >>> iso_is_valid('RUS')
    True
    >>> iso_is_valid('a2c')
    False
    >>> iso_is_valid('RUSS')
    False
    >>> iso_is_valid('OWID_KOS')
    True
    """
    if code == 'OWID_KOS':
        return True
    
    # check if the code has 3 characters
    elif len(code) != 3:
        return False
    
    # check if the characters are letters
    for char in code:
        if char not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
           return False
        
    return True



# DEFINE CLASS
class Country:
    """
    Represents a country.
    
    Instance attributes: iso_code (str), name (str), continents (list),
                         co2_emissions (dict), population (dict)
    Class attributes: min_year_recorded, max_year_recorded
    Instance methods: __str__, __lt__, add_yearly_data, get_co2_emissions_by_year,
                      get_population_by_year, get_co2_per_capita_by_year, get_historical_co2
    Class method: get_country_from_data
    Static methods: get_countries_by_continent, get_total_historical_co2_emissions,
                    get_total_co2_emissions_per_capita_by_year, get_co2_emissions_per_capita_by_year,
                    get_historical_co2_emissions, get_top_n
    """
    min_year_recorded = float('inf')
    max_year_recorded = float('-inf')
    
    def __init__(self, iso_code, name, continents, year, co2_emissions, population):
        """ (Country, str, str, list, int, float, int) -> Country
        Creates an object of type Country with corresponding attributes.
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> r.name
        'Russia'
        >>> r.iso_code
        'RUS'
        
        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 2006, 1.553, 56578000)
        >>> c.co2_emissions
        {2006: 1.553}
        
        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.min_year_recorded
        1949
        """
        # check is the iso code is valid
        if iso_is_valid(iso_code):
            self.iso_code = iso_code
        else:
            raise AssertionError
        
        # initialize attributes
        self.name = name
        
        self.continents = copy.copy(continents)
        
        if co2_emissions != -1:
            self.co2_emissions = {year : co2_emissions}
        else:
            self.co2_emissions = {}
            
        if population != -1:
            self.population = {year : population}
        else:
            self.population = {}
        
        # update min and max year recorded if necessary
        if year < Country.min_year_recorded:
            Country.min_year_recorded = year
        elif year > Country.max_year_recorded:
            Country.max_year_recorded = year


    def __str__(self):
        """ (Country) -> str

        The method returns a string representation of a country containing the name,
        the continents, and a string representation of both the o2_emissions dictionary
        and the population dictionary.
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> str(r)
        'Russia\\tASIA,EUROPE\\t{2007: 1604.778}\\t{2007: 14266000}'
        
        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 2006, 1.553, 56578000)
        >>> str(c)
        'Democratic Republic of Congo\\tAFRICA\\t{2006: 1.553}\\t{2006: 56578000}'
        
        >>> s = Country("SEN", "Senegal", ["AFRICA"], 1971, 1.351, 4388000)
        >>> str(s)
        'Senegal\\tAFRICA\\t{1971: 1.351}\\t{1971: 4388000}'
        """
        # retrive attributes from the country
        str_components = [self.name]
        str_components.append(",".join(self.continents))
        str_components.append(str(self.co2_emissions))
        str_components.append(str(self.population))
        
        # return a concatenation of the components
        return "\t".join(str_components)


    def __lt__(self, other):
        """ (Country, Country) -> bool
        
        Returns True if the name of self comes before the name of other in alphabetical order,
        False otherwise.
        
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        
        >>> b < r
        True
        >>> b < q
        True
        >>> r < q
        False
        >>> q < r
        True
        """        
        # return whether self is alphabetically first out of the two
        return self.name < other.name

        
    def add_yearly_data(self, data):
        """ (Country, str) -> NoneType
        
        The method updates the appropriate attributes of the country.
        It also updates the min and max year recorded if necessary.
        
        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> a.co2_emissions == {1949: 0.015, 2018: 9.439}
        True
        >>> a.population == {1949: 7663783, 2018: 37122000}
        True
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> r.add_yearly_data("2000\\t\\t1000000")
        >>> r.co2_emissions == {2007: 1604.778}
        True
        >>> Country.min_year_recorded
        1949
        
        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 2006, 1.553, 56578000)
        >>> c.add_yearly_data("1930\\t1.234\\t56000000")
        >>> Country.min_year_recorded
        1930
        """
        # separate the data into its category
        individual_data = data.split("\t")
        year = int(individual_data[0])
        co2_emission = individual_data[1]
        population = individual_data[2]
        
        # update the Country object's attributes
        if co2_emission != '':
            self.co2_emissions[year] = float(co2_emission)
        if population != '' and population != '\n':
            self.population[year] = int(population)
        
        # update the min and max year recorded if necessary
        if year < Country.min_year_recorded:
            Country.min_year_recorded = year
        
        elif year > Country.max_year_recorded:
            Country.max_year_recorded = year


    def get_co2_emissions_by_year(self, year):
        """ (Country, int) -> float
        
        The method takes as input an integer representing a year.
        It return the co2 emission of the country in the specified year.
        If not available, it returns 0.0.
        
        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> a.get_co2_emissions_by_year(1949)
        0.015

        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 2006, 1.553, 56578000)
        >>> c.add_yearly_data("1930\\t1.234\\t56000000")
        >>> c.get_co2_emissions_by_year(1930)
        1.234
        >>> c.get_co2_emissions_by_year(2006)
        1.553
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> r.get_co2_emissions_by_year(2020)
        0.0
        """
        # retrieve the co2 emission of that year
        try:
            emission = self.co2_emissions[year]
        # in case the data is unavailable
        except KeyError:
            emission = 0.0
        
        # return the co2 emission of that year
        return emission
        

    def get_population_by_year(self, year):
        """ (Country, int) -> float
        
        The method takes as input an integer representing a year.
        It return the population of the country in the specified year.
        If not available, it returns 0.0.
        
        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> a.get_population_by_year(1949)
        7663783

        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 2006, 1.553, 56578000)
        >>> c.add_yearly_data("1930\\t1.234\\t56000000")
        >>> c.get_population_by_year(1930)
        56000000
        >>> c.get_population_by_year(2006)
        56578000
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> r.get_population_by_year(2020)
        0.0
        """
        # retrieve the population of that year
        try:
            population = self.population[year]
        # in case the data is unavailable
        except KeyError:
            population = 0.0
        
        # return the population of that year
        return population
    
    
    def get_co2_per_capita_by_year(self, year):
        """ (Country, int) -> float
        
        The method takes as input an integer representing a year.
        It returns the co2 emission per capita in tonnes for the specified year.
        It returns None if some of the required data is missing.
        
        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, -1, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> round(a.get_co2_per_capita_by_year(2018), 5)
        0.25427

        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 2006, 1.553, 56578000)
        >>> c.add_yearly_data("1930\\t1.234\\t56000000")
        >>> round(c.get_co2_per_capita_by_year(2006), 5)
        0.02745
        >>> round(c.get_co2_per_capita_by_year(1930), 5)
        0.02204
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, -1)
        >>> n = r.get_co2_per_capita_by_year(2006)
        >>> print(n)
        None
        >>> n = r.get_co2_per_capita_by_year(2007)
        >>> print(n)
        None
        """
        # retrieve relevant data
        total_co2_emission = self.get_co2_emissions_by_year(year) * 10**6
        population = self.get_population_by_year(year)
        
        # in case one of the data is missing
        if total_co2_emission == 0.0 or population == 0.0:
            return None
        
        # compute and return the co2 emission per capita
        co2_per_capita = total_co2_emission / population
        return co2_per_capita
        
        
    def get_historical_co2(self, year):
        """ (Country, int) -> float
        
        The method takes as input an integer representing a year.
        It returns the historical co2 emission in millions of tonnes that the country
        has produced for all years up to and including the specified year.
        
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> q.add_yearly_data("1993\\t30.985\\t501000")
        >>> q.add_yearly_data("1989\\t14.292\\t462000")
        >>> q.get_historical_co2(2000)
        45.277
        
        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 2006, 1.553, 56578000)
        >>> c.add_yearly_data("1930\\t1.234\\t56000000")
        >>> c.get_historical_co2(1930)
        1.234
        >>> c.get_historical_co2(2020)
        2.787
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, -1, 500000)
        >>> r.get_historical_co2(2020)
        0.0
        """
        # initialize variable
        historical_co2 = 0.0
        
        # retrieve all co2 emission data
        co2_items = self.co2_emissions.items()
        co2_data = list(co2_items)
        
        # add relevant data to the sum
        for data_year, emission in co2_data:
            if data_year <= year:
                historical_co2 += emission
                
        # return the sum
        return historical_co2
        
    
    @classmethod
    def get_country_from_data(cls, data):
        """ (str) -> Country
        
        The method takes as input a string storing data about a country.
        It returns a new Country object created from the data in the input string.
        
        >>> a = Country.get_country_from_data("ALB\\tAlbania\\tEUROPE\\t1991\\t4.283\\t3280000")
        >>> a.__str__()
        'Albania\\tEUROPE\\t{1991: 4.283}\\t{1991: 3280000}'
        
        >>> r = Country.get_country_from_data("RUS\\tRussia\\tASIA,EUROPE\\t1971\\t1533.262\\t130831000")
        >>> r.continents
        ['ASIA', 'EUROPE']
        >>> str(r)
        'Russia\\tASIA,EUROPE\\t{1971: 1533.262}\\t{1971: 130831000}'
        
        >>> a = Country.get_country_from_data("AFG\\tAfghanistan\\tASIA\\t1949\\t\\t7663783")
        >>> a.name
        'Afghanistan'
        >>> a.co2_emissions == {}
        True
        >>> a.population == {1949: 7663783}
        True
        """
        # sort the data
        columns = data.split("\t")
        
        iso_code = columns[0]
        name = columns[1]
        continents = columns[2].split(",")
        year = int(columns[3])
        try:
            co2_emissions = float(columns[4])
        except ValueError:
            co2_emissions = -1
        try:
            population = int(columns[5])
        except ValueError:
            population = -1
        
        # create new Country object
        return cls(iso_code, name, continents, year, co2_emissions, population)
    
    
    @staticmethod
    def get_countries_by_continent(countries):
        """ (list) -> dict
        
        The method takes as input a list of objects of type Country.
        It returns a dictionary mapping a string representing a continent to
        a list of countries from the input list that are in that continent.

        >>> a = Country("AFG", "Afghanistan", ["ASIA"], 1949, 0.015, 7663783)
        >>> a.add_yearly_data("2018\\t9.439\\t37122000")
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> c = [a, b, r]
        >>> d = Country.get_countries_by_continent(c)
        >>> str(d['ASIA'][1])
        'Russia\\tASIA,EUROPE\\t{2007: 1604.778}\\t{2007: 14266000}'
        
        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 2006, 1.553, 56578000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> d = Country.get_countries_by_continent([c, r, q])
        >>> len(d["ASIA"])
        2
        >>> len(d["EUROPE"])
        1
        >>> len(d["AFRICA"])
        1
        
        >>> d = Country("DNK", "Denmark", ["EUROPE"], 1906, 6.554, 2746271)
        >>> d.add_yearly_data("2000\\t1.000\\t123456789")
        >>> s = Country("ESP", "Spain", ["EUROPE"], 1932, 21.182, 23969738)
        >>> f = Country("FRA", "France", ["EUROPE"], 2000, 416.07, 59015000)
        >>> x = Country.get_countries_by_continent([d, s, f])
        >>> len(x["EUROPE"])
        3
        >>> str(x["EUROPE"][0])
        'Denmark\\tEUROPE\\t{1906: 6.554, 2000: 1.0}\\t{1906: 2746271, 2000: 123456789}'
        >>> x["EUROPE"][1].name
        'Spain'
        >>> x["EUROPE"][2].name
        'France'
        >>> len(x["ASIA"])
        Traceback (most recent call last):
        KeyError: 'ASIA'
        """
        # initialize an emtpy dictionary
        countries_by_continent = {}
        
        # sort every country according to their continent(s)
        for country in countries:
            for continent in country.continents:
                
                # in case there is already a key with such continent
                if continent in countries_by_continent:
                    countries_by_continent[continent].append(country)
                    
                # in case there is no key with such continent
                else:
                    countries_by_continent[continent] = [country]
        
        # return the dictionary
        return countries_by_continent


    @staticmethod
    def get_total_historical_co2_emissions(countries, year):
        """ (list, int) -> float
        
        The method takes as input a list of objects of type Country, and an integer
        representing a year.
        It returns a float representing the total co2 emissions (in millions of tonnes)
        produced by all the countries in the input list for all years up to
        and uncluding the specified year.
        
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> b.add_yearly_data("1991\\t4.283\\t3280000")
        >>> q.add_yearly_data("1993\\t30.985\\t501000")
        >>> q.add_yearly_data("1989\\t14.292\\t462000")
        >>> c = [b, r, q]
        >>> Country.get_total_historical_co2_emissions(c,2007)
        1721.161
        
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> q.add_yearly_data("1993\\t30.985\\t501000")
        >>> q.add_yearly_data("1989\\t14.292\\t462000")
        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 2006, 1.553, 56578000)
        >>> c.add_yearly_data("1930\\t1.234\\t56000000")
        >>> Country.get_total_historical_co2_emissions([q, c], 2000)
        46.511
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, -1, 500000)
        >>> Country.get_total_historical_co2_emissions([r], 2020)
        0.0
        """
        # initialize variable
        total_co2_emissions = 0.0
        
        # compute the historical co2 emission per country
        for country in countries:
            individual_co2_emission = country.get_historical_co2(year)
            # add value to the sum
            total_co2_emissions += individual_co2_emission
        
        # return the sum
        return total_co2_emissions
        
        
    @staticmethod
    def get_total_co2_emissions_per_capita_by_year(countries, year):
        """ (list, int) -> float

        The method takes as input a list of objects of type Country, and an integer
        representing a year.
        It returns the co2 emissions per capita in tonnes produced by the countries
        in the input list in the specified year.
        If a required data is missing, then the country is excluded from the list.
        
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> c = [b, r]
        >>> round(Country.get_total_co2_emissions_per_capita_by_year(c,2007), 5)
        92.98855
        
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> q.add_yearly_data("1993\\t30.985\\t501000")
        >>> q.add_yearly_data("1989\\t14.292\\t462000")
        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 1993, 1.553, 56578000)
        >>> round(Country.get_total_co2_emissions_per_capita_by_year([q, c], 1993), 5)
        0.57005
        >>> round(Country.get_total_co2_emissions_per_capita_by_year([q, c], 1989), 5)
        30.93506
        
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 0, 1218000)
        >>> Country.get_total_co2_emissions_per_capita_by_year([q], 1989)
        0.0
        >>> Country.get_total_co2_emissions_per_capita_by_year([q], 2007)
        0.0
        """
        # initialize variable
        total_co2 = 0.0
        total_population = 0
        
        # compute the co2 emission per capita and population per country
        for country in countries:
            # check if the data is available for the given year
            if year in country.co2_emissions and year in country.population:
                total_co2 += country.co2_emissions[year]
                total_population += country.population[year]
            
        # compute and return the co2 emissions per capita
        try:
            total_co2_per_capita = (total_co2 * 10**6) / total_population
        except ZeroDivisionError:
            return 0.0
        
        return total_co2_per_capita
        
        
    @staticmethod
    def get_co2_emissions_per_capita_by_year(countries, year):
        """ (list, int) -> dict
        
        The method takes as input a list of objects of type Country, and an integer
        representing a year.
        It returns a dictionary mapping objects of type Country to floats representing
        the co2 emissions per capita in tonnes produced by the country in the specified year.
        
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> b.add_yearly_data("1991\\t4.283\\t3280000")
        >>> c = [b, r]
        >>> d1 = Country.get_co2_emissions_per_capita_by_year(c,2007)
        >>> len(d1)
        2
        >>> round(d1[r], 5)
        112.4897
        
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> q.add_yearly_data("1993\\t30.985\\t501000")
        >>> q.add_yearly_data("1989\\t14.292\\t462000")
        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 1993, 1.553, 56578000)
        >>> d2 = Country.get_co2_emissions_per_capita_by_year([q,c], 1993)
        >>> len(d2)
        2
        >>> round(d2[q],5)
        61.84631
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, -1)
        >>> d3 = Country.get_co2_emissions_per_capita_by_year([r], 2007)
        >>> len(d3)
        1
        >>> print(d3[r])
        None
        """
        # initialize an empty dictionary
        co2_emissions_per_capita = {}
        
        # compute the co2 emission per capita for each country
        for country in countries:
            co2_emission = country.get_co2_per_capita_by_year(year)
            # add the data to the dictionary
            co2_emissions_per_capita[country] = co2_emission
        
        # return the dictionary
        return co2_emissions_per_capita
        
        
    @staticmethod
    def get_historical_co2_emissions(countries, year):
        """ (list, int) -> dict
        
        The method takes as input a list of objects of type Country, and an integer
        representing a year.
        It returns a dictionary mapping objects of type Country to floats representing
        the total co2 emissions (in millions of tones) produced by that country for all
        years up to and including the specified year.
        
        >>> b = Country("ALB", "Albania", ["EUROPE"], 2007, 3.924, 3034000)
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, 14266000)
        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> b.add_yearly_data("1991\\t4.283\\t3280000")
        >>> q.add_yearly_data("1993\\t30.985\\t501000")
        >>> q.add_yearly_data("1989\\t14.292\\t462000")
        >>> c = [b, r, q]
        >>> d1 = Country.get_historical_co2_emissions(c,2007)
        >>> len(d1)
        3
        >>> d1[q]
        108.176

        >>> q = Country("QAT", "Qatar", ["ASIA"], 2007, 62.899, 1218000)
        >>> q.add_yearly_data("1993\\t30.985\\t501000")
        >>> q.add_yearly_data("1989\\t14.292\\t462000")
        >>> c = Country("COD", "Democratic Republic of Congo", ["AFRICA"], 1993, 1.553, 56578000)
        >>> d2 = Country.get_historical_co2_emissions([q, c], 2020)
        >>> len(d2)
        2
        >>> d2[q]
        108.176
        >>> d2[c]
        1.553
        
        >>> r = Country("RUS", "Russia", ["ASIA", "EUROPE"], 2007, 1604.778, -1)
        >>> d3 = Country.get_historical_co2_emissions([q, c, r], 2020)
        >>> len(d3)
        3
        >>> d2[q]
        108.176
        >>> d4 = Country.get_historical_co2_emissions([q, c, r], 1000)
        >>> len(d4)
        3
        >>> d4[q]
        0.0
        >>> d4[c]
        0.0
        """
        # initialize an empty dictionary
        historical_co2_emissions = {}
        
        # compute the historical co2 emission for each country
        for country in countries:
            co2_emission = country.get_historical_co2(year)
            # add the data to the dictionary
            historical_co2_emissions[country] = co2_emission
        
        # return the dictionary
        return historical_co2_emissions
        
        
    @staticmethod
    def get_top_n(dict_of_countries, n):
        """ (dict, int) -> list
        
        The method takes as input a dictionary mapping objects of type Country
        to numbers, and an interger.
        The method returns a list of tuples where each tuple is made up by the
        iso code of a country and the number to which the country is mapped
        in the input dictionary.
        
        >>> a = Country("ALB", "Albania", [], 0, 0.0, 0)
        >>> b = Country("AUT", "Austria", [], 0, 0.0, 0)
        >>> c = Country("BEL", "Belgium", [], 0, 0.0, 0)
        >>> d = Country("BOL", "Bolivia", [], 0, 0.0, 0)
        >>> e = Country("BRA", "Brazil", [], 0, 0.0, 0)
        >>> f = Country("IRL", "Ireland", [], 0, 0.0, 0)
        >>> g = Country("MAR", "Marocco", [], 0, 0.0, 0)
        >>> h = Country("NZL", "New Zealand", [], 0, 0.0, 0)
        >>> i = Country("PRY", "Paraguay", [], 0, 0.0, 0)
        >>> j = Country("PER", "Peru", [], 0, 0.0, 0)
        >>> k = Country("SEN", "Senegal", [], 0, 0.0, 0)
        >>> l = Country("THA", "Thailand", [], 0, 0.0, 0)
        >>> d1 = {a: 5, b: 5, c: 3, d: 10, e: 3, f: 9, g: 7, h: 8, i: 7, j: 4, k: 6, l: 0}
        
        >>> t = Country.get_top_n(d1, 10)
        >>> t[:5]
        [('BOL', 10), ('IRL', 9), ('NZL', 8), ('MAR', 7), ('PRY', 7)]
        >>> t[5:]
        [('SEN', 6), ('ALB', 5), ('AUT', 5), ('PER', 4), ('BEL', 3)]
        
        >>> d2 = {a: 1, b: 1, c: 1, d: 1, e: 1, f: 1, g: 1, h: 1, i: 1, j: 1, k: 1, l: 1}
        >>> Country.get_top_n(d2, 5)
        [('ALB', 1), ('AUT', 1), ('BEL', 1), ('BOL', 1), ('BRA', 1)]
        
        >>> d3 = {a: 10, g: 4, h: 3, i: 4, j: 2, k: 7, l: 1}
        >>> Country.get_top_n(d3, 3)
        [('ALB', 10), ('SEN', 7), ('MAR', 4)]
        """
        # initialize variables
        reverse_dict = {}
        nums = []
        count = 0
        list_of_tuples = []
        
        # create a dictionary mapping numbers to countries with that associated num
        for country in dict_of_countries:
            # in case there is already a key with that num
            if dict_of_countries[country] in reverse_dict:
                reverse_dict[dict_of_countries[country]].append(country)
            # in case there is no key with that num
            else:
                reverse_dict[dict_of_countries[country]] = [country]
                # update the list of num
                nums.append(dict_of_countries[country])
        
        # sort the list of num in descending order
        nums.sort()
        nums = nums[ : : -1]
        
        # sort the countries for each num in the reverse dict in alphabetical order
        for country_list in reverse_dict:
            reverse_dict[country_list].sort()
            
        # create the top n countries by appending the new tuple
        # according to the order sorted previously (largest num, then alphabetical)
        for num in nums:
            for country in reverse_dict[num]:
                list_of_tuples.append((country.iso_code, num))
                
                # update count and break if int n is reached
                count += 1
                if count == n:
                    break
            if count == n:
                break
        
        # return the list of tuples
        return list_of_tuples
        
       
# DEFINE FUNCTION
def get_countries_from_file(filename):
    """ (str) -> dict
    
    The function takes as input a string representing a filename.
    It returns a dictionary mapping ISO country codes to objects of type Country
    base on the data in the file.
    
    >>> d1 = get_countries_from_file("small_co2_data.tsv")
    >>> len(d1)
    9
    >>> str(d1['ALB'])
    'Albania\\tEUROPE\\t{2002: 3.748}\\t{2002: 3126000}'
    
    >>> fobj = open("continent_test4.txt", "w", encoding= "UTF-8")
    >>> fobj.write('TUR\\tTurkey\\tASIA,EUROPE\\t1900\\t1.037\\t14030306')
    42
    >>> fobj.close()
    >>> d2 = get_countries_from_file("continent_test4.txt")
    >>> len(d2)
    1
    >>> str(d2['TUR'])
    'Turkey\\tASIA,EUROPE\\t{1900: 1.037}\\t{1900: 14030306}'
    
    >>> d3 = get_countries_from_file("large_co2_data.tsv")
    >>> len(d3['SEN'].co2_emissions)
    61
    >>> len(d3['CUB'].co2_emissions)
    78
    """
    # initialize an empty dictionary
    dict_by_iso_codes = {}
    
    # read the file
    fobj= open(filename, "r", encoding= "UTF-8")
    
    # update dictionary according to the data found on its line
    for line in fobj:
        # separate the data into columns
        columns = line.split("\t")
        
        # in case there is already a Country object associated with such country
        if columns[0] in dict_by_iso_codes:
            country = dict_by_iso_codes[columns[0]]
            country.add_yearly_data("\t".join(columns[3 : ]))
        # in case there is no Country object associated with such country
        else:
            new_country = Country.get_country_from_data(line)
            dict_by_iso_codes[new_country.iso_code] = new_country
    
    # close the file and return the dictionary
    fobj.close()    
    return dict_by_iso_codes
    
    

# TEST MODULE
if __name__ == "__main__":
    doctest.testmod()