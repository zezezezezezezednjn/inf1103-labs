print("=============")
print("Welcome here")
print("First post here")
print ("============")

username = "cool_creator"
bio = "Fun Blogger"
followers = 100

followers += 50
print("Day 1:", followers)

followers += 20
print("Day 2:", followers)

followers -= 10
print("Day 3:", followers)

print("Username:", username)
print("Bio:", bio)
print("Followers:", followers)

username = input("Enter username: ")
age =int(input("Enter age: "))
category = input("Enter content category: ")

print("\nInstagram Profile")
print("====================")
print("username:", username)
print("age:", age)
print("category:", category)

if age>40 and category == "fun":
    print("You are old what is fun for you???")