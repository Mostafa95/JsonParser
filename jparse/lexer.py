from .constants import *


def lex_str(input, startInd):
    if input[startInd] != JSON_QUOTE:
        return None,startInd
    startInd+=1
    ans = ''
    strLen = len(input)
    for i in range(startInd,strLen):
        if input[i]==JSON_QUOTE:
            break
        ans+= input[i]
    return ans, startInd + len(ans) + 1


def lex_bool(input, startInd):
    if input[startInd:startInd+4] == 'true':
        return True,startInd+4
    if input[startInd:startInd+5] == 'false':
        return False,startInd+5

    return None, startInd  


def lex_num(input, startInd):
    if input[startInd] != '-' and (input[startInd]<'0' or input[startInd]>'9'):
        return None, startInd
    sign=1
    if input[startInd] == '-':
        sign = -1
        startInd+=1
        
    ans = ''
    strLen = len(input) 
    for i in range(startInd,strLen):
        if input[i]>='0' and input[i]<='9':
            ans+=input[i]
        else:
            break
    ansNum = int(ans) * sign
    return ansNum, startInd + len(ans)


def getToken(inputStr, ind):
    extracted_str, newInd = lex_str(inputStr,ind)
    if extracted_str is not None:
       return extracted_str,newInd
    
    extracted_str, newInd = lex_num(inputStr,ind)
    if extracted_str is not None:
        return extracted_str,newInd
    
    extracted_str, newInd = lex_bool(inputStr,ind)
    if extracted_str is not None:
        return extracted_str,newInd
    
    extracted_str, newInd = lex_arr(inputStr,ind)
    if extracted_str is not None:
        return extracted_str,newInd
    
    extracted_str, newInd = lex_obj(inputStr,ind)
    if extracted_str is not None:
        return extracted_str,newInd
    return None,newInd


def lex_arr_rec(inputStr, ind, tokens):
    if inputStr[ind] == JSON_RIGHTBRACKET:
        tokens.append(inputStr[ind])
        return ind+1
    while ind < len(inputStr):
        extracted_str, ind = getToken(inputStr,ind)
        if extracted_str is not None:
            tokens.append(extracted_str)
            continue
        if inputStr[ind] == 'n' and inputStr[ind:ind+4] == 'null':
            tokens.append(None)
            ind +=4
        elif inputStr[ind] == JSON_WHITESPACE or inputStr[ind] == JSON_NEWLINE:
            ind+=1
        elif inputStr[ind] in JSON_COMMA:
            tokens.append(inputStr[ind])
            ind+=1
        elif inputStr[ind] == JSON_RIGHTBRACKET:
            tokens.append(inputStr[ind])
            ind+=1
            break
        else:
            raise Exception("Unexpected char")
    return ind


def lex_obj_rec(inputStr, ind, tokens):
    if inputStr[ind] == JSON_RIGHTBRACE:
        tokens.append(inputStr[ind])
        return ind+1
    while ind < len(inputStr):
        extracted_str, ind = getToken(inputStr,ind)
        if extracted_str is not None:
            tokens.append(extracted_str)
            continue
        if inputStr[ind] == 'n' and inputStr[ind:ind+4] == 'null':
            tokens.append(None)
            ind +=4
        elif inputStr[ind] == JSON_WHITESPACE or inputStr[ind] == JSON_NEWLINE:
            ind+=1
        elif inputStr[ind] in JSON_SYNTAX:
            tokens.append(inputStr[ind])
            ind+=1
        elif inputStr[ind] == JSON_RIGHTBRACE:
            tokens.append(inputStr[ind])
            ind+=1
            break
        else:
            raise Exception("Unexpected char")
    return ind


def lex_arr(input,ind):
    if input[ind]!=JSON_LEFTBRACKET:
        return None, ind
    tokens = [input[ind]]
    newInd = lex_arr_rec(input,ind+1,tokens)
    return tokens, newInd


def lex_obj(input,ind):
    if input is None or ind>=len(input) or input[ind]!=JSON_LEFTBRACE:
        return None, ind
    tokens = [ input[ind] ]
    newInd = lex_obj_rec(input,ind+1,tokens)
    return tokens,newInd


def lex(inputStr):
    return lex_obj(inputStr,0)[0]
