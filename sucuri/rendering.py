import json, os

def template(filename, obj=None):
    local = os.getcwd()
    arq = open(local + '/' + filename, 'r')
    text = arq.readlines()
    space = 0
    tabulation = 0
    tags = []
    result = ''

    for textline in text :
        ctrl = transform(textline, obj)
        
        if ctrl[1] != '|':
            tags.append(ctrl[1])

            if space == 0 and spaces(textline) > 0:
                tabulation = spaces(textline) - space
            
            if tabulation > 0 and space >= spaces(textline):
                quantity = ((space - spaces(textline)) / tabulation) + 1

                if quantity == 0 and len(tags) > 0 and space > 0:
                    lastreg = len(tags) -2
                    result += '</' + tags[lastreg] + '>'
                    tags.pop(lastreg)

                for i in reversed(range(0, int(quantity))):
                    lastreg = len(tags) -2
                    result += '</' + tags[lastreg] + '>'
                    tags.pop(lastreg)
        
        else:
            msg = textline.strip()
            ctrl[0] = msg.replace('|','\n')

        result += ctrl[0]

        space = spaces(textline)

    arq.close()
    for i in reversed(range(len(tags))):
        result += '</' + str(tags[i]) + '>'
    return result

def spaces(text):
    result = 0
    for i in range(len(text)):
        if text[i] != ' ':
            result = i
            break
    return result

def transform(text, obj=None):
    msg = text.strip()
    properties = ''
    txt = ''

    if obj:
        while instr(msg, '{') > 0:
            data = substring(msg, instr(msg, '{'), instr(msg, '}') +1)
            elem = substring(data, 1, len(data)-1).strip()
            if elem in obj:
                msg = msg.replace(data, str(obj[elem]))

    tag = msg

    if '(' in msg:
        tag = substring(msg, 0, instr(msg, '('))
        properties = ' ' + substring(msg, instr(msg, '(') +1, instr(msg, ')'))
        if instr(msg, ')') +1 != len(msg):
            txt = substring(msg, instr(msg, ')') +2, len(msg) )
            
    elif ' ' in msg:
        tag = substring(msg, 0, instr(msg, ' '))
        if instr(msg, ' ') +1 != len(msg):
            txt = substring(msg, instr(msg, ' ') +1, len(msg) )

    result = '<' + tag + properties + '>' + txt

    return [result, tag]

def instr(text, char):
    result = 0
    if char in text:
        for i in range(len(text)):
            if text[i] == char:
                result = i
                break
    return result

def substring(text, ini, end):
    size = len(text)
    result = ''
    if ini >= 0 and end > 0 and size > 0 and end > ini:
        end = end - size
        if end != 0:
            result = text[ini:end]
        else:
            result = text[ini:]
    return result