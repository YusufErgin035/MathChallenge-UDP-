import random

def question(n):
    processtime = random.randint(2,4)
    answer = str(random.randint(1,20))
    for _ in range(processtime):
        randprocs = random.randint(1, 3)
        var = random.randint(1, 20)
        match randprocs:
            case 1:
                answer += f" + {var}"
            case 2:
                answer += f" - {var}"
            case 3:
                answer += f" * {var}"
    print(f"{n}. Soru: {answer} = ?")
    return eval(answer)