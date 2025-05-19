import random

def question(n):
    processtime = random.randint(2,4)
    question = str(random.randint(1,20))
    for _ in range(processtime):
        randprocs = random.randint(1, 3)
        var = random.randint(1, 20)
        match randprocs:
            case 1:
                question += f" + {var}"
            case 2:
                question += f" - {var}"
            case 3:
                question += f" * {var}"
    print(f"{n}. Soru: {question} = ?")
    return eval(question)