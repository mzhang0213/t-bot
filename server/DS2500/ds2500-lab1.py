# LAB EXERCISE 01
# Problem 1
# . Assign the value 25 to a variable named num.
num = 25
# . Assign the string "Computer Science" to a variable called subject.
subject = "Computer Science"
# . Assign a boolean value True to a variable named is_active.
is_active = True 

# Problem 2
# . Assign the string "Data Science" to a variable called text.
text = "Data Sceince"
# . Extract the first character of text and assign it to a variable called first_char.
first_char = text[0]

# . Extract the last character of text and assign it to a variable called last_char.
last_char = text[-1]
# . Find the length of text and and assign it to a variable called text_length.
text_length = len(text)
# . Convert text to uppercase and assign it to a variable called text_upper.
text_upper = text.upper()

# . Extract the word "Science" from text and assign it to a variable called second_word.
second_word = text.split()[1]

# . Replace "Data" with "Computer" and assign the replaced text to a variable called text1.
text1 = text.replace("Data", "Computer")



# Problem 3
# . Create a list fruits which contains 3 fruits in this order: "banana", "apple", and "orange".
fruits = ["banana", "apple", "orange"]

# . Add "grapes" to the list using the .append() method.
fruits.append("grapes")
# . Change the item, "apple", to "mango".
fruits[1] = "mango"

# . Extract the first element of fruits and assign it to a variable named first_item.
first_item = fruits[0]
# . Extract the last element of fruits and assign it to a variable named last_item.
last_item = fruits[-1]

# Problem 4
spam = """Spam spam Spam spam Spam spam Spam Spam Spam spam spams spams
spams spams spams spams spams Spam Spam Spam Spams Spam spam spam Spam
spams spams Spam Spam Spam Spams Spam spam spam Spam spams spam spam spams
spams"""

# . Count how many times "Spam" appears in the spam and assign the count to a variable named
# count_Spam.
count_Spam = spam.count("Spam")
# . Count how many times "spam" appears in the spam and assign the count to a variable named
# count_spam.
count_spam = spam.count("spam")
# . Count how many times "spams" appears in the spam and assign the count to a variable named
# count_spams.
count_spam = spam.count("spams")
# . Modify spam so that it contains only the lowercase word "spam" separated by spaces, and store the
# cleaned string in a variable named spam_clean.
spam_clean = spam.lower().replace("spams", "spam")
# . Count how many "spam" appears in the spam_clean and assign the count to a variable named
# count_spam_clean.
count_spam_clean = spam_clean.count("spam")

# . Convert spam_clean into a list that contains each word (i.e., spam) using a string method, and
# assign the list to a variable named spam_list.
spam_list = spam_clean.split()

# . Count the total number of items in spam_list and assign it to a variable named count_items.
count_items = len(spam_list)

# . Use list slicing to get a list of 4 spams (i.e., ["spam","spam","spam","spam"]) and assign the
# sliced list into a variable named spam_list_sliced. You may slice any way you'd like in order to get
# the final output
spam_list_sliced = spam_list[:4]
