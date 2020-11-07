from enum import Enum
from random import choice, randint
import os
import time

questions_this_session = 0

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
    os.system("cls")
    os.system("clear")

class QuestionType(Enum):
    BASE_CONVERSION = 0,
    BUS_STOP_DIVISION = 1,
    BASE_ADDITION = 2,
    BINARY_FRACTION = 3,
    FRAME_BUFFER_MEMORY = 4,
    DOT_FREQUENCY = 5,
    TWOS_COMP = 6
    
class BaseType(Enum):
    DEC = "DECIMAL / DENARY (Base10)"
    HEX = "HEXADECIMAL (Base16)"
    BIN = "BINARY (Base2)"
    OCT = "OCTAL (Base8)"

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

while True:
    ClearTerminal()
    GiveQuestion(choice(list(QuestionType)))