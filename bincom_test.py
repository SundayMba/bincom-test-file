import statistics
import psycopg2 
import random

"""
    Building a python Data structure representation
    of the HTML web content using python dictionary.

    packages to install:
    psycopg2-binary: pip install psycopg2-binary
"""

colors_from_web = {
    "MONDAY": ["GREEN", "YELLOW", "GREEN", "BROWN", "BLUE", "PINK", "BLUE", "YELLOW", "ORANGE", "CREAM", "ORANGE", "RED", "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "GREEN"],
    "TUESDAY": ["ARSH", "BROWN", "GREEN", "BROWN", "BLUE", "BLUE", "BLEW", "PINK", "PINK", "ORANGE", "ORANGE", "RED", "WHITE", "BLUE", "WHITE", "WHITE", "BLUE", "BLUE", "BLUE"],
    "WEDNESDAY": ["GREEN", "YELLOW", "GREEN", "BROWN", "BLUE", "PINK", "RED", "YELLOW", "ORANGE", "RED", "ORANGE", "RED", "BLUE", "BLUE", "WHITE", "BLUE", "BLUE", "WHITE", "WHITE"],
    "THURSDAY": ["BLUE", "BLUE", "GREEN", "WHITE", "BLUE", "BROWN", "PINK", "YELLOW", "ORANGE", "CREAM", "ORANGE", "RED", "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "GREEN"],
    "FRIDAY": ["GREEN", "WHITE", "GREEN", "BROWN", "BLUE", "BLUE", "BLACK", "WHITE", "ORANGE", "RED", "RED", "RED", "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "WHITE"]
}

# combining the colors for the days to form a list of colors for simple data analysis
all_colors = []
for day, colors in colors_from_web.items():
    all_colors.extend(colors)

"""
building a hashmap (dictionary) of the frequency of each color.
"""
colors_frequency = {}
for color in all_colors:
    if color in colors_frequency:
        colors_frequency[color] += 1
    else:
        colors_frequency[color] = 1

"""
1. Which color of shirt is the mean color?

to calculate mean mathematically requires a numeric list of data not strings of colors.
so it will be dificult to calculate the mean of the colors since no numeric representation
of the colors were given.

But if i interpret the question to be the most frequent occurring color in the week, that will be
the mode, which question number 2 address.

2. Which color is mostly worn throughout the week?
"""

# 1. Which color of shirt is the mean color?
mean_color = None
mean_value = 0
for color, value in colors_frequency.items():
    if value > mean_value:
        mean_value = value
        mean_color = color
print(f'mean color: {mean_color}')

# 2. Which color is mostly worn throughout the week?
""" Answer:
    
    the mean color which is the most frequent occurring
    color is the mostly worn throughout the week.

    from the HTML web page given, BLUE is the mean color which is the most worn color in the week.
"""

# 3. Which color is the median?
"""
    Answer:

    we have to sort the colors in ascending order.
"""

sorted_colors = sorted(all_colors)
start = 0
end = len(sorted_colors)
mid_point = (start + end) // 2 # integer division 
median = sorted_colors[mid_point]

print(f"median color: {median}")


# 4. Get the variance of the colors
colors_frequencies = colors_frequency.values()
color_variance = statistics.variance(colors_frequencies)
print(f"Color Variance: {color_variance}")

# 5.  if a colour is chosen at random, what is the probability that the color is red?

number_of_red_colors = colors_frequency.get("RED")
total_colors = len(all_colors)
probability_of_red = number_of_red_colors / total_colors
prob_in_percent = probability_of_red * 100
print(f"probability of red: {probability_of_red:.3f} or {prob_in_percent:.2f}%")

# 6 Save the colours and their frequencies in postgresql database

"""
    I will assume that the database has already been created. 
    so i will only connect to it.
"""

def save_to_database(colors_counter: dict):
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="your_db_name",
            user="your_username",
            password="your_password"
        )
        cursor = connection.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS color_frequencies (
                id SERIAL PRIMARY KEY,
                color VARCHAR(50),
                frequency INTEGER
            )
        """)

        # Insert color data
        for color, frequency in colors_counter.items():
            cursor.execute(
                "INSERT INTO color_frequencies (color, frequency) VALUES (%s, %s)",
                (color, frequency)
            )

        connection.commit()
        cursor.close()
        connection.close()
        print("Data saved to PostgreSQL successfully.")
    
    except Exception as error:
        print("Error saving to PostgreSQL:", error)

# Save the colors and their frequencies
save_to_database(colors_frequency)


# 7.  BONUS write a recursive searching algorithm to search for a number entered by user in a list of numbers.

"""
    I will be using a binary search algorithm instead of linear because of it's efficiency.
"""

def search_recursively(arr: list, start: int, end: int, target: int):
    """Recursive search using binary search algorithm
    
    Keyword arguments:
    argument
        arr: list of numbers
        start: start index
        end: end index of the list
        target: number to search for
    Return: -1 not found or number if found.
    """
    
    if start > end:
        return -1
    
    mid = (start + end ) // 2
    if target == arr[mid]:
        return mid
    elif target > arr[mid]:
        return search_recursively(arr, mid + 1, end, target)
    else:
        return search_recursively(arr, start, mid - 1, target)
    
# Example usage
numbers_list = [3, 5, 7, 9, 11, 13, 17]
target_number = int(input("Enter a number to search: "))
search_result = search_recursively(numbers_list, 0, len(numbers_list) - 1, target_number)
if search_result != -1:
    print(f"Number {target_number} found at index {search_result}.")
else:
    print(f"Number {target_number} not found.")
    

# 8.  Write a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10.
number = [random.choice("01") for _ in range(4)]
binary_number = ''.join(number)
decimal_number = int(binary_number, base=2)
print(f'decimal Number: {decimal_number} and binary number: {binary_number}')


# 9. Write a program to sum the first 50 fibonacci sequence.
def fibonacci_sum(number):
    """find sum of first 50 fib
    
    Keyword arguments:
    argument
        number: set to 50
    Return: number
    """
    a, b = 0, 1
    total = 0
    for _ in range(number):
        total += a
        a, b = b, a + b
    return total    

fibonacci_total = fibonacci_sum(50)
print(f"Sum of the first 50 Fibonacci numbers: {fibonacci_total}")