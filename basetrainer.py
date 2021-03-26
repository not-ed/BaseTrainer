from enum import Enum
from random import choice, randint, shuffle
import os
import time
import math
import platform
from urllib import request

questions_this_session = 0
version_message = ""

# This should be changed alongside the 'VERSION' file with each push to allow for version checking at startup.
VERSION_SUM = "f3204e2a4b263a7e4e4959c937fc5da5fbbc9524356f764ebd717c443ce99fec"


class Question():
    prompt = ""
    answer = ""
    start_time = 0
    final_time = ""

    def __init__(self,prompt_text,answer_text):
        self.prompt = prompt_text
        self.answer = answer_text
        global questions_this_session
        questions_this_session += 1

    def PrintDivider(self):
        print("-"*32)

    def Display(self):
        self.PrintDivider()
        print(self.prompt)
        self.StartTimer()
        self.PrintDivider()
        self.WaitForUserReveal()
        self.ShowAnswer()
        self.StopTimer()
        self.DisplayStats()
        self.WaitForUserContinue()

    def ShowAnswer(self):
        self.PrintDivider()
        print("The answer is: {}".format(self.answer))
        self.PrintDivider()
    
    def WaitForUserReveal(self):
        input("Press 'Enter' to reveal the answer.")

    def WaitForUserContinue(self):
        input("Press 'Enter' to display the next question.")
        ClearTerminal()

    def StartTimer(self):
        self.start_time = time.time()
    
    def StopTimer(self):
        time_taken = 0 + int(time.time() - self.start_time)
        mins_taken = int(time_taken / 60)
        seconds_taken = int(time_taken - (mins_taken * 60))
        self.final_time = "{}m {}s".format(mins_taken,seconds_taken)

    def DisplayStats(self):
        global questions_this_session
        print("You spent {} on this question.".format(self.final_time))
        print("You have practiced {} question{} this session.".format(questions_this_session,str("s" * (questions_this_session > 1))))
        self.PrintDivider()

    
def ClearTerminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

class QuestionType(Enum):
    BASE_CONVERSION = 0,
    BUS_STOP_DIVISION = 1,
    BASE_ADDITION = 2,
    BINARY_FRACTION = 3,
    FRAME_BUFFER_MEMORY = 4,
    DOT_FREQUENCY = 5,
    TWOS_COMP = 6,
    #Semester 2 onwards
    MODE_SET = 7,
    MEDIAN_SET = 8,
    MEAN_SET = 9,
    RANGE_SET = 10
    MATRIX_MULTIPLICATION = 11,
    MATRIX_TRANSPOSE = 12,
    MATRIX_ORDER = 13,
    MATRIX_DETERMINANT = 14,
    MATRIX_SUM = 15

class BaseType(Enum):
    DEC = "DECIMAL / DENARY (Base10)"
    HEX = "HEXADECIMAL (Base16)"
    BIN = "BINARY (Base2)"
    OCT = "OCTAL (Base8)"

# Check for the most up to date version
def PerformVersionCheck():
    global version_message
    global VERSION_SUM
    try:
        utd_version_sum = request.urlopen("https://raw.githubusercontent.com/not-ed/BaseTrainer/main/VERSION")
        if utd_version_sum.read().decode('utf-8') == VERSION_SUM:
            version_message = "*BaseTrainer is up to date.*"
        else:
            version_message = "*A NEW VERSION OF BASETRAINER IS AVAILABLE FROM GITHUB:*\nhttps://github.com/not-ed/BaseTrainer"
    except:
        version_message = "*Unable to check for newest version.*"

    #Returns two base types guaranteed to be different
def GetRandomBaseTypePair():
    first = 0
    second = 0
    while (first == second):
        first =choice(list(BaseType))
        second = choice(list(BaseType))
    return (first,second)

def FormatNumberToBase(num,base):
    if base == BaseType.HEX:
        return (str(hex(num))[2:].upper())
    elif base == BaseType.BIN:
        return (str(bin(num))[2:])
    elif base == BaseType.OCT:
        return (str(oct(num))[2:])
    else:
        return str(num)

def GiveBaseConversionQuestion():
    raw_number = randint(0,100000)
    bases = GetRandomBaseTypePair()
    given_number = FormatNumberToBase(raw_number,bases[0]) #base-converted number user is first given
    answer_number = FormatNumberToBase(raw_number,bases[1]) #answer user needs to convert to
    direct_notice = "\n\nPlease make the conversion directly.\nDO NOT convert to other bases to work out your answer." * randint(0,1)

    q_text = "Convert this {} number into a {} number:\n\n{}{}\n".format(bases[0].value,bases[1].value,given_number,direct_notice)
    a_text = answer_number
    
    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveBusStopQuestion():
    number = randint(100,9999)
    divider = randint(2,9)
    raw_answer = int(number / divider)
    raw_remainder = int(number % divider)

    q_text = "Calculate the following, and express with a remainder:\n{}\n{}|{}\n".format((" "*(len(str(divider))+1))+("_"*len(str(number))),divider,number)
    a_text = "{}, remainder {}".format(raw_answer,raw_remainder)

    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveAdditionQuestion():
    number = [randint(0,1677721),randint(0,1677721)]
    answer = number[0] + number[1]
    base = choice([BaseType.BIN,BaseType.HEX,BaseType.OCT])
    display_number = [FormatNumberToBase(number[0],base),FormatNumberToBase(number[1],base)]

    if(len(display_number[0]) < len(display_number[1])):
        display_number[0] = " "*(len(display_number[1])-len(display_number[0]))+display_number[0]
        display_number = list(reversed(display_number))
    elif(len(display_number[0]) > len(display_number[1])):
        display_number[1] = " "*(len(display_number[0])-len(display_number[1]))+display_number[1]

    display_answer = FormatNumberToBase(answer,base)
    
    q_text = "Calculate the following {} values.\nPlease make this calculation directly, DO NOT convert to other bases to work out your answer.\n\n  {}\n+ {}\n".format(base.value,display_number[0],display_number[1])
    a_text = display_answer
    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveBinaryFractionQuestion():
    exponent_bin = ""
    mantissa_bin = ""
    exponent_dec = 0
    mantissa_dec = 0

    for i in range(randint(4,10)):
        bit = randint(0,1)
        exponent_bin = str(bit) + exponent_bin
        exponent_dec += bit*(2**i)

    exponent_bin = str(exponent_bin)
    for i in exponent_bin:
        if(i == "0"):
            exponent_bin = exponent_bin[1:]
        else:
            break

    for i in range(randint(1,6)):
        bit = randint(0,1)
        mantissa_bin += str(bit)
        mantissa_dec += bit*(2**(-(i+1)))
    
    mantissa_dec = str(mantissa_dec)[2:]

    mantissa_bin = str(mantissa_bin)[::-1]
    for i in mantissa_bin:
        if(i == "0"):
            mantissa_bin = mantissa_bin[1:]
        else:
            break
    mantissa_bin = str(mantissa_bin)[::-1]
    
    swap_flag = randint(0,1)
    if(swap_flag): #Decimal to Binary Fraction
        q_text = "Convert this {} value into a Binary Fraction:\n\n{}.{}\n".format(BaseType.DEC.value,exponent_dec,mantissa_dec)
        a_text = "{}.{}".format(exponent_bin,mantissa_bin)
    else: #Binary Fraction to Decimal
        q_text = "Convert this Binary Fraction into a {} value:\n\n{}.{}\n".format(BaseType.DEC.value,exponent_bin,mantissa_bin)
        a_text = "{}.{}".format(exponent_dec,mantissa_dec)
    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveFrameBufferQuestion():
    width = randint(16,15360)
    height = randint(16,8640)

    in_bytes = randint(0,1)

    color_depths = [1,2,4,8,16,24,30,32,36,48] #X-bit color
    bit_depth = choice(list(color_depths))

    answer = (width*height)*bit_depth

    labels = [["BITS","b"],["BYTES","B"]]

    if in_bytes:
        answer = float(answer) / 8 #8 bits = 1 Byte

    q_text = "How many {} of memory are required to hold the information of a:\n\n{} x {} frame/image with {}-BIT COLOR?\n".format(labels[in_bytes][0],width,height,bit_depth)
    a_text = "{}{}".format(str(answer),labels[in_bytes][1])
    generated_question = Question(q_text,a_text)
    generated_question.Display()


def GiveDotFrequencyQuestion():
    width = randint(16,15360)
    height = randint(16,8640)

    rates = [15,30,50,55,60,70,75,76,85,95,100,120,144,155,165,166,170,175,180,185,200,240,280]
    ref_rate = choice(list(rates))

    answer = (width*height)*ref_rate

    q_text = "What is the DOT FREQUENCY of a:\n\n{} x {} display with a REFRESH RATE of {}Hz?\n".format(width,height,ref_rate)
    a_text = "{} pixels per second".format(answer)
    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveTwosCompQuestion():
    question_number = randint(1,254)
    question_bin_raw = bin(question_number)
    question_bin = "0b"
    for i in str(question_bin_raw)[2:].zfill(8):
        if i == "1":
            question_bin = question_bin + "0"
        elif i == "0":
            question_bin = question_bin + "1"
    
    question_bin = bin(int(question_bin,2))
    question_bin = bin(int(question_bin,2) + 1)

    q_text = "Represent the following number as an 8-bit binary number using 2's Complement:\n\n-{}\n".format(question_number)
    a_text = str(question_bin)[2:].zfill(8)

    generated_question = Question(q_text,a_text)
    generated_question.Display()


# Semester 2 onwards
def GiveModeSetQuestion():    
    answer_count = randint(1,3)
    # If more than one answer exists in the question, acts as a count of how many of each there will be.
    answer_value_individual_counts = randint(2,3)
    additional_set_size = randint(answer_count*answer_value_individual_counts + 4,answer_count*answer_value_individual_counts + 8)
    # Appropriate text to use based on how many numbers must be identified in the question
    mode_indicator_text = [choice(("MODE","MODAL VALUE")),"BIMODAL VALUES", "MULTIMODAL VALUES"]

    data = []
    answer_values = []

    for i in range(answer_count):
        answer_values.append(randint(1,150))
        for j in range(answer_value_individual_counts):
            data.append(answer_values[i])
    
    for i in range(additional_set_size - len(data)):
        unique = False
        filler_value = 0
        while not unique:
            filler_value = randint(1,150)
            for j in range(len(data)):
                if filler_value == data[j]: # Cannot be the same as an answer
                    unique = False
                    break
                else:
                    unique = True
        data.append(filler_value)

    shuffle(data)

    data_string = ""
    for i in range(len(data)):
        data_string  += str(data[i]) + "  "

    answer_string = ""
    for i in range(answer_count):
        if i == answer_count - 1 and answer_count != 1:
            answer_string += " and "
        elif i != 0:
            answer_string += ", "
        answer_string += str(answer_values[i])

    q_text = "Identify the {} of the following data set:\n{}".format(mode_indicator_text[answer_count-1],data_string)
    a_text = answer_string

    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveMedianSetQuestion():
    set_size = randint(3,10)
    data_sorted = []
    lowest_number = randint(1,50)
    for i in range(set_size):
        data_sorted.append(lowest_number)
        lowest_number += randint(1,20)
    
    data_shuffled = data_sorted.copy()
    shuffle(data_shuffled)
    median = 0

    if set_size % 2 == 0:
        median = (data_sorted[int((set_size)/2)-1]+data_sorted[int((set_size)/2)])
        median = median / 2
    else:
        median = (data_sorted[math.floor(set_size/2)])

    if median - int(median) == 0: #is an integer
        median = int(median)

    data_string = ""
    for i in range(set_size):
        data_string  += str(data_shuffled[i]) + "  "

    q_text = "Identify the MEDIAN of the following data set:\n{}".format(data_string)
    a_text = str(median)

    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveMeanSetQuestion():
    range_size = randint(4,10)
    data = []
    total = 0

    for i in range(range_size):#not an integer
        data.append(randint(1,150))
        total += data[i]

    data_string = ""
    for i in range(range_size):
        data_string  += str(data[i]) + "  "


    q_text = "Identify the MEAN of the following data set:\n{}".format(data_string)
    a_text = str((1.0 * total)/range_size)

    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveRangeSetQuestion():
    range_size = randint(5,13)
    if range_size % 2 == 0:
        range_size = range_size + 1

    lowest = randint(2,30)
    difference = randint(range_size,125)
    highest = lowest + difference

    low_i = 0
    high_i = 0

    while low_i == high_i:
        low_i = randint(0,range_size-1)
        high_i = randint(0,range_size-1)

    data_string = ""
    for i in range(range_size):
        if i == low_i:
            data_string += str(lowest)
        elif i == high_i:
            data_string += str(highest)
        else:
            data_string += str(randint(lowest,highest))
        data_string += "  "

    q_text = "Identify the RANGE of the following data set:\n{}".format(data_string)
    a_text = str(difference)

    generated_question = Question(q_text,a_text)
    generated_question.Display()


def GiveMatrixMultiplicationQuestion():
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    matrice_dimension_sizes = [randint(2,4),randint(2,4),randint(2,4)]

    a_l_i = randint(0,24) 
    b_l_i = a_l_i + 1

    m_a = []
    m_b = []

    for i in range(matrice_dimension_sizes[0]):        
        m_a.append([])
        for j in range(matrice_dimension_sizes[1]):
            m_a[i].append(randint(1,9))

    for i in range(matrice_dimension_sizes[1]):        
        m_b.append([])
        for j in range(matrice_dimension_sizes[2]):
            m_b[i].append(randint(1,9))

    # How far to seperate both matrices from each other on screen
    q_distance = max(matrice_dimension_sizes)

    q_text = "Calculate {}{}".format(letters[a_l_i],letters[b_l_i])
    q_text += "\n{} =".format(letters[a_l_i]) + ("  "*len(m_a[0]))+" {} =".format(letters[b_l_i])
    for i in range(q_distance):
        current_line = "\n"
        if(i <= len(m_a)-1):
            if i == 0:
                current_line += "┌ "
            elif i == len(m_a)-1:
                current_line += "└ " 
            else:
                current_line += "│ "
        
            for k in range(len(m_a[i])):
                current_line += str(m_a[i][k]) + " "

            if i == 0:
                current_line += "┐ " 
            elif i == len(m_a)-1:
                current_line += "┘ " 
            else:
                current_line += "│ "
        else:
            current_line += "  " * (q_distance+2)

        if(i <= len(m_b)-1):
            if i == 0:
                current_line += "┌ " 
            elif i == len(m_b)-1:
                current_line += "└ " 
            else:
                current_line += "│ "
        
            for k in range(len(m_b[i])):
                current_line += str(m_b[i][k]) + " "

            if i == 0:
                current_line += "┐ " 
            elif i == len(m_b)-1:
                current_line += "┘ "
            else:
                current_line += "│ "

        q_text += current_line

    # Actual meat of solving the matrix multiplication
    answer = []
    for i in range(matrice_dimension_sizes[0]): #matrix A's height / mds index 0
        answer.append([])
        for j in range(matrice_dimension_sizes[2]): #matrix B's width / mds index 2
            index_total = 0
            for k in range(matrice_dimension_sizes[1]): #matrix A's width/matrix B's height (mds index 1)
                index_total += (m_a[i][k] * m_b[k][j])
            answer[i].append(index_total)

    a_text = ""
    for i in range(len(answer)):
        row_text = ""
        for j in range(len(answer[i])):
            row_text += str(answer[i][j]).rjust(3," ") + " "
        if i == 0:
            a_text += "\n┌ {}┐\n".format(row_text)
        elif i == matrice_dimension_sizes[0]-1:
            a_text += "└ {}┘".format(row_text)
        else:
            a_text += "│ {}│\n".format(row_text)

    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveMatrixTranspositionQuestion():
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    letter_index = randint(0,25)

    matrix_dimensions = [randint(2,5)]
    matrix_dimensions.append(randint(2,5))

    original_matrix = []
    for i in range(matrix_dimensions[0]):
        original_matrix.append([])
        for j in range(matrix_dimensions[1]):
            original_matrix[i].append(str(randint(1,9) * choice([-1,1])).rjust(2," "))

    transposed_matrix = []
    for i in range(matrix_dimensions[1]): #original matrix WIDTH
        transposed_matrix.append([])
        for j in range(matrix_dimensions[0]): #original matrix HEIGHT
            transposed_matrix[i].append(original_matrix[j][i])
    
    original_string = ""
    for i in range(len(original_matrix)):
        row_text = ""
        for j in range(len(original_matrix[i])):
            row_text += str(original_matrix[i][j]).rjust(2," ") + " "
        if i == 0:
            if(len(original_matrix) == 1):
                original_string  += "[ {}]\n".format(row_text)
            else:
                original_string  += "┌ {}┐\n".format(row_text)
        elif i == matrix_dimensions[0]-1:
            original_string  += "└ {}┘".format(row_text)
        else:
            original_string  += "│ {}│\n".format(row_text)

    transposed_string = "\n"
    for i in range(len(transposed_matrix)):
        row_text = ""
        for j in range(len(transposed_matrix[i])):
            row_text += str(transposed_matrix[i][j]).rjust(2," ") + " "
        if i == 0:
            if(len(transposed_matrix) == 1):
                transposed_string  += "[ {}]\n".format(row_text)
            else:
                transposed_string  += "┌ {}┐\n".format(row_text)
        elif i == matrix_dimensions[1]-1:
            transposed_string  += "└ {}┘".format(row_text)
        else:
            transposed_string  += "│ {}│\n".format(row_text)

    q_text = "Determine {}ᵀ\n{}=\n{}".format(letters[letter_index],letters[letter_index],original_string) # ᵀ or chr(7488)
    a_text = transposed_string

    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveMatrixOrderQuestion():
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    letter_index = randint(0,25)

    width = randint(2,5)
    height = randint(2,5)

    q_matrix = ""

    for i in range(height):
        row_text = ""
        for j in range(width):
            row_text += str(randint(-9,9)).rjust(2," ") + " "
        if i == 0:
            q_matrix  += "┌ {}┐\n".format(row_text)
        elif i == height-1:
            q_matrix  += "└ {}┘".format(row_text)
        else:
            q_matrix  += "│ {}│\n".format(row_text)

    q_text = "Determine the {} of {}\n{}=\n{}".format(choice(("SIZE","ORDER")),letters[letter_index],letters[letter_index],q_matrix)
    a_text = "{} x {}".format(str(height),str(width))

    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveMatrixDeterminantQuestion():
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    letter_index = randint(0,25)
    # Only a 2x2 matrix is assumed to be within the scope of the cirriculum based on notes given.
    numbers = [randint(1,9),randint(1,9),randint(1,9),randint(1,9)]
    determinant = (numbers[0] * numbers[3]) - (numbers[1] * numbers[2])
    
    q_text = choice(("Calculate |{}|".format(letters[letter_index]),"Calculate the DETERMINANT of {}".format(letters[letter_index])))
    q_text = q_text + "\n" + letters[letter_index] + "=\n"
    q_text = q_text + "┌ {} {} ┐\n".format(str(numbers[0]),str(numbers[1]))
    q_text = q_text + "└ {} {} ┘".format(str(numbers[2]),str(numbers[3]))
    a_text = str(determinant)

    generated_question = Question(q_text,a_text)
    generated_question.Display()

def GiveMatrixSumQuestion():
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    l_a = randint(0,24)
    l_b = l_a + 1
    matrix_dimensions = [randint(2,4),randint(2,4)]
    m_a = []
    m_b = []
    answer = []
    use_subtraction = randint(0,1) # 0 = add, 1 = sub
    swap_matrices = randint(0,1) # Only relevant if subtraction is used

    for i in range(matrix_dimensions[0]):
        i_a = []
        i_b = []
        i_ans = []
        for j in range(matrix_dimensions[1]):
            i_a.append(randint(1,30))
            i_b.append(randint(1,30))
            if use_subtraction:
                if swap_matrices:
                    i_ans.append(i_b[j] - i_a[j])
                else:
                    i_ans.append(i_a[j] - i_b[j])
            else:
                i_ans.append(i_a[j] + i_b[j])
        m_a.append(i_a)
        m_b.append(i_b)
        answer.append(i_ans)

    q_text = ""
    a_text = "\n"
    if swap_matrices:
        q_text = "Calculate {}{}{}\n".format(letters[l_b],["+","-"][use_subtraction],letters[l_a])
    else:
        q_text = "Calculate {}{}{}\n".format(letters[l_a],["+","-"][use_subtraction],letters[l_b])
    
    q_text = q_text + "{}=".format(letters[l_a]) + (" "*(3*matrix_dimensions[1]+(matrix_dimensions[1]+1))) + "{}=".format(letters[l_b]) + "\n"

    for i in range(matrix_dimensions[0]):
        q_row_text_a = ""
        q_row_text_b = ""
        q_row_text_answer = ""
        for j in range(matrix_dimensions[1]):
            q_row_text_a = q_row_text_a + str(m_a[i][j]).rjust(3, " ") + " "
            q_row_text_b = q_row_text_b + str(m_b[i][j]).rjust(3, " ") + " "
            q_row_text_answer = q_row_text_answer + str(answer[i][j]).rjust(3, " ") + " "

        if i == 0:
            q_text = q_text + "┌{}┐ ┌{}┐\n".format(q_row_text_a,q_row_text_b)
            a_text = a_text + "┌{}┐\n".format(q_row_text_answer)
        elif i == matrix_dimensions[0]-1:
            q_text = q_text + "└{}┘ └{}┘".format(q_row_text_a,q_row_text_b)
            a_text = a_text + "└{}┘".format(q_row_text_answer)
        else:
            q_text = q_text + "│{}│ │{}│\n".format(q_row_text_a,q_row_text_b)
            a_text = a_text + "│{}│\n".format(q_row_text_answer)

    # Reminder that may appear when subtraction is being asked in the question.
    q_text = q_text + ("\nRemember, Matrix Subtraction is NOT commutative!" * (use_subtraction * (randint(0,5) == 0)))
    
    generated_question = Question(q_text,a_text)
    generated_question.Display()

#Specify a question type, it will handle the rest
def GiveQuestion(question_type):
    if(question_type == QuestionType.BASE_CONVERSION):
        GiveBaseConversionQuestion()
    if(question_type == QuestionType.BUS_STOP_DIVISION):
        GiveBusStopQuestion()
    if(question_type == QuestionType.BASE_ADDITION):
        GiveAdditionQuestion()
    if(question_type == QuestionType.BINARY_FRACTION):
        GiveBinaryFractionQuestion()
    if(question_type == QuestionType.FRAME_BUFFER_MEMORY):
        GiveFrameBufferQuestion()
    if(question_type == QuestionType.DOT_FREQUENCY):
        GiveDotFrequencyQuestion()
    if(question_type == QuestionType.TWOS_COMP):
        GiveTwosCompQuestion()
    #Semester 2 onwards
    if(question_type == QuestionType.MODE_SET):
        GiveModeSetQuestion()
    if(question_type == QuestionType.MEDIAN_SET):
        GiveMedianSetQuestion()
    if(question_type == QuestionType.MEAN_SET):
        GiveMeanSetQuestion()
    if(question_type == QuestionType.RANGE_SET):
        GiveRangeSetQuestion()
    if(question_type == QuestionType.MATRIX_MULTIPLICATION):
        GiveMatrixMultiplicationQuestion()
    if(question_type == QuestionType.MATRIX_TRANSPOSE):
        GiveMatrixTranspositionQuestion()
    if(question_type == QuestionType.MATRIX_ORDER):
        GiveMatrixOrderQuestion()
    if(question_type == QuestionType.MATRIX_DETERMINANT):
        GiveMatrixDeterminantQuestion()
    if(question_type == QuestionType.MATRIX_SUM):
        GiveMatrixSumQuestion()


# Program Start

# Ask for user topic range
PerformVersionCheck()
print(version_message + "\n" + "-"*32)
print("Do you want to include or exclude any particular semester's topics?")
print("     1. Only practice Semester 1 related topics")
print("     2. Only practice Semester 2 related topics")
print("     3. Practice all related topics")
selection = 0
while selection < 1 or selection > 3:
    selection_raw = input()
    if selection_raw.isnumeric():
        selection = int(selection_raw)
    

while True:
# 0-6 is SEM 1
    ClearTerminal()
    if selection == 1:
        GiveQuestion(choice(list(QuestionType)[:6]))
    elif selection == 2:
        GiveQuestion(choice(list(QuestionType)[7:]))
    if selection == 3: #All Topics
        GiveQuestion(choice(list(QuestionType)))
