input = 371

inputString = str(input);

lenInput = len(inputString);
if (lenInput != 0) :
    sum = 0
    for num in inputString:
        sum += (int(num) ** lenInput)

    if input == sum :
        if lenInput == 3:
            print("Armstrong, equal to 3 digits")
        elif lenInput < 3:
            print("Armstrong, less than 3 digits")
        else:
            print("Armstrong, More than 3 digits")
    else :
        if lenInput == 3:
            print("Not Armstrong, equal to 3 digits")
        elif lenInput < 3:
            print("Not Armstrong, less than 3 digits")
        else:
            print("Not Armstrong, More than 3 digits")


def konvergen(rerata, prev_rerata):
    if rerata == prev_rerata:
        return True
    return False

rerata = 1
prev_rerata = 1
if konvergen(rerata, prev_rerata):
    print("konvergen")
else:
    print("Tidak")



