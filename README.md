# final_lab_dm
У лабораторній роботі створено скінченний автомат для перевірки регулярних виразів за патерном State. Реалізовано класи AsciiState для літер і цифр, DotState для будь-якого символу, а також обгортки StarState і PlusState які зациклюють попередні стани для операторів повторення. Клас RegexFSM компілює вираз і будує ланцюг переходів. Перевірка цільових стрічок виконується через пошук у глибину dfs, що забезпечує коректний бектрекінг при недетермінованих розгалуженнях.


запуск
1. перейти в поточну папку
2. python3 code.py

Тести та результати:
    regex_pattern = "a*4.+hi"

    regex_compiled = RegexFSM(regex_pattern)

    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))  # True
    print(regex_compiled.check_string("meow"))  # False

    regex = "1*2+3."
    regex_compiled = RegexFSM(regex)
    print(regex_compiled.check_string("111223x")) # True
    print(regex_compiled.check_string("23!"))     # True
    print(regex_compiled.check_string("113y"))    # False
    print(regex_compiled.check_string("223"))     # False
