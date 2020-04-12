import sys
import os.path
import os
kanaCharacters = ['あ', 'ア', 'か', 'カ', 	'さ','サ', 	'た','タ' 	,'な','ナ', 'は','ハ', 	'ま','マ', 	'や','ヤ', 	'ら','ラ', 
                'わ','ワ', 'い','イ', 'き','キ', 'し','シ', 'ち','チ', 'に','ニ', 'ひ','ヒ', 'み','ミ', '※', 'り','リ', 'ゐ','ヰ', 
                'う','ウ', 	'く','ク', 	'す','ス', 	'つ','ツ', 	'ぬ','ヌ', 	'ふ','フ', 	'む','ム', 	'ゆ','ユ', 	'る','ル',
                'ん','ン', 'お', 'オ', 'こ','コ', 'そ','ソ', 'と','ト', 'の','ノ', 'ほ','ホ', 'も','モ', 'よ','ヨ', 'ろ','ロ', 'を',
                'ヲ', 'え','エ', 'け','ケ', 'せ','セ', 'て','テ', 'ね','ネ', 'へ','ヘ', 'め','メ',   'れ','レ', 'ゑ','ヱ', 'が','ガ',
                'ざ','ザ', 'だ','ダ',	'ば','バ',	'ぱ','パ',	'か゚', 'カ゚', 'ぎ','ギ',	'じ','ジ'	'ぢ','ヂ',	'び','ビ',	'ぴ','ピ',	'き゚','キ゚',
                'ぐ','グ',	'ず', 'ズ',	'づ', 'ヅ',	'ぶ', 'ブ',	'ぷ', 'プ',	'く゚', 'ク゚',  'げ', 'ゲ',	'ぜ', 'ゼ',	'で', 'デ',	'べ', 'ベ',	'ぺ', 
                'ペ', 'け゚', 'ケ゚',  'ご', 'ゴ',	'ぞ', 'ゾ',	'ど', 'ド',	'ぼ', 'ボ',	'ぽ', 'ポ',	'こ゚', 'コ゚']
def add_kana_to_kanji(x):
    global line
    if ("</rt></ruby>" in line): #check to see if rt ruby is in the line. 
            line = line.replace("</rt></ruby>", ",")
            subdivide = line.split(",")
            extra_chars = ''
            for i in range(len(subdivide[1])-1):
                for y in kanaCharacters:
                    if subdivide[1][i] == y:
                        kana_char = y
                        extra_chars += y
                        subdivide[1] = subdivide[1].replace(y, " ")
            line=subdivide[0]+extra_chars+','+subdivide[1]
            line = line.replace("<rt style=\";font-size:50%\">", extra_chars+',')

def add_kana_to_reading(x):
    global line
    divide = line.split(",")
    if "," in line and divide[0][0] in kanaCharacters:
        if (ord(divide[0][1])-ord(divide[1][1])!=96):
            i = 0
            extra_chars = ''
            while divide[0][i] in kanaCharacters:
                extra_chars+= divide[0][i]
                one = str(divide[1])
                i+=1
            line = divide[0]+','+extra_chars+one+','+divide[2]

def no_kanji(x):
    global line
    divide = line.split("\t")
    list_line = list(line)
    counter = 0
    for x in divide[0]:
        if (19968<=ord(x)<=40879): #if a kanji
            counter+=1
    if (',' and '<br>' not in line and list_line[0] in kanaCharacters and len(divide)==2 and counter==0):
        line = ','+ divide[0] + ',' + divide[1]

def br_case(x): #case in which there is a <br> in the line
    global line
    if "<br>" in line:
        line = line.replace("<br>", ",")
        line = line.replace("\n", '')
        divide = line.split("\t")
        line = divide[1]
        div = line.split(',')
        line = divide[0] + ','+div[0] + ',' + div[1] + '\n' #puts in correct order

def super_special(x):
    global line
    division = line.split("<rt style=\";font-size:50%\">")
    lst = []
    for x in division:
        lst.append(x.split("</rt></ruby>"))
    word_with_kanji = ''
    kana_reading = ''
    yeet = 0
    for x in range(len(lst)-1):
        if x > 0: yeet = 1
        word_with_kanji+=lst[x][yeet]
    for y in lst[-1][1]:
        if y in kanaCharacters:
            word_with_kanji+=y
    for n in line:
        if n in kanaCharacters:
            kana_reading+=n
    reading = ''   
    kana_chars = ''
    lst_of_chars = [i for i in lst[-1][1] if i not in kanaCharacters]
    str1 = ''.join(lst_of_chars)
    str1 = str1.replace("\t", "")
    str1 = str1.replace("\n", "")
    english = str1
    line = word_with_kanji + ',' + kana_reading + ',' + english + '\n'

def reformat(x):
    global line
    line = line.replace("\t", '')
    line = line.replace('\n', '')  
    divide = line.split(',')
    line = divide[1] + ',' + divide[2] + ',,' + divide[0] + ',,\n'

file1 = sys.argv[1]
with open(file1, encoding='utf-8') as fh:
    x = fh.readlines()
# print("printing line by line....")
for l in range(len(x)):
    
    line = x[l].replace(",", ";").replace("<ruby style=\"-webkit-ruby-position: before;\">", "") 
    if line.count('<rt style=')<2:
        """Below is the first special case that we will deal with. This is the
        case in which the reading has been seperated from the kanji. i.e., formatting
        looks like  読、よ、める, to read... and める　should be part of both よ and 読"""
        add_kana_to_kanji(line) #gonna modify our line

        """This is the second special case that we will test for. This is the case in which a line
        begins with kana, and looks like --> この結果, けっか, consequently; as a result <-- in which
        only the KANJI's reading has been put into the kana section. So, we need to add the preceding
        kana to the entire reading of the word/phrase"""
        add_kana_to_reading(line)

        """This is the case in which there is no kanji on the line, """
        no_kanji(line)

        br_case(line)
        #another special case 取り,とり, 組り,く, multiple replaces happened so it breaks the word...
    
    else:
        super_special(line)

    reformat(line)
     
    print(line)

# save_path= '~/Desktop'
# stringTosave = (line)
# completed = os.path.join(save_path, word_list+'.txt')
# file1 = open(completed, "w")



