from .constants import *

def validateForm(tokens):
    if tokens is None or len(tokens)==0:
        return False
    
    tokenStack = []
    for token in tokens:
        if token ==  JSON_LEFTBRACKET or token == JSON_LEFTBRACE:
            tokenStack.append(token)            
        if token == JSON_RIGHTBRACKET:
            if(tokenStack[-1] == JSON_LEFTBRACKET):
                tokenStack.pop()
        if token == JSON_RIGHTBRACE:
            if(tokenStack[-1] == JSON_LEFTBRACE):                
                tokenStack.pop()
    return len(tokenStack)==0

def parse_obj(tokens, ind):
    ans = {}

    if tokens[ind] == JSON_RIGHTBRACE:
        return ans

    while True:
        if (type(tokens[ind]) != str and type(tokens[ind]) != list) or tokens[ind] in JSON_BLACKLIST:
            raise Exception('Unexpected char')
        key = tokens[ind]
        ind+=1
        
        if tokens[ind] != JSON_COLON:
            raise Exception('Expected colon after key in object, got: {}'.format(tokens[ind]))
        ind+=1
        
        # to be modified
        if type(tokens[ind]) != str and type(tokens[ind]) != int and \
            type(tokens[ind]) != bool and tokens[ind] is not None and\
            type(tokens[ind])!= list:
            raise Exception('Unexpected char')
        
        if type(tokens[ind])==list and tokens[ind][0]==JSON_LEFTBRACKET:
            value = parse_arr(tokens[ind],1)
        elif type(tokens[ind])==list and tokens[ind][0]==JSON_LEFTBRACE:
            value = parse_obj(tokens[ind],1)
        else:
            value = tokens[ind]
        ind+=1
        
        ans[key]=value
        
        if tokens[ind]==JSON_RIGHTBRACE:
            break
        if tokens[ind]==JSON_COMMA:
            ind+=1
            continue
        raise Exception('Expected comma after pair in object, got: {}'.format(tokens[ind]))
    return ans

def parse_arr(tokens, ind):
    ans = []
    
    if tokens[ind] == JSON_RIGHTBRACKET:
        return []

    while True:
        if (type(tokens[ind]) != str and type(tokens[ind]) != list) or tokens[ind] in JSON_BLACKLIST:
            raise Exception('Unexpected char '+str(tokens[ind])+' {}'.format(ind))
        
        if type(tokens[ind]) == list and tokens[ind][0]==JSON_LEFTBRACKET:
            ans.append(parse_arr(tokens[ind],1))
        elif type(tokens[ind]) == list and tokens[ind][0]==JSON_LEFTBRACE:
            ans.append(parse_obj(tokens[ind],1))
        else:
            ans.append(tokens[ind])
        ind+=1
        if tokens[ind]==JSON_COMMA:
            ind+=1
            continue
        elif tokens[ind]==JSON_RIGHTBRACKET:
            break
        else:
            raise Exception('Unexpected char '+str(tokens[ind])+' {}'.format(ind))
        
        
    return ans
    
def parse(tokens):
    validForm = validateForm(tokens)
    if validForm == False:
        raise Exception(INVALIDMESSAGE)
    
    ans = parse_obj(tokens,1)
    return ans
