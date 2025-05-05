import hangManUtil as hu, secrets

words = [
    "ultra", "superstar", "beige", "utility", "problematic", "success", "ambitious"
]
word = secrets.choice(words)
stage = -1
answer = list()

for letter in word:
    answer.append('_')
print(f"""Your word is: {"".join(answer)}""")


while stage < 5:
    index = 0
    flag = 0
    userLetter = input("Input the next letter: ")
    
    for letter in word:
        if userLetter == letter:
            answer[index] = word[index]
            flag = 1

        index += 1
    
    print(f"""Current answer: {"".join(answer)}""")
    print("+++++++++++++++++++++++++++++")

    if ''.join(answer) == word:
        print("You win!")
        break

    if flag == 0:
        stage += 1
        print(hu.stages[stage])
        print(f"""Current answer: {"".join(answer)}\n+++++++++++++++++++++++++++++""")
        if stage == 5:
            print("He ded! Game over!") 


print("Run program again to play!")







