#Tanveer Muttaqueen
#tanveer.mutta@gmail.com


import re
import json
import javalang


'''
X509Certificate -> X509 Certificate
X509Der -> X509 Der
XX509Der -> XX 509 Der
i18n -> i18 n
N4JS -> N4 JS
i4 -> i4
hell405 -> hell 405
'''
def tokenize_with_str_int_str( token):
    #p = re.compile( r'([_a-zA-Z]{2,})(\d+)([_a-zA-Z]+)|([_a-zA-Z]{2,})(\d+)|([_a-zA-Z]\d+)([_a-zA-Z]+)' )
    p = re.compile( r'([a-zA-Z]+)(\d+)([a-zA-Z]+)(\d+)([a-zA-Z]+)|([a-zA-Z]{2,})(\d+)([a-zA-Z]+)(\d+)|([a-zA-Z]{2,})(\d+)([a-zA-Z]+)|([a-zA-Z]\d+)([a-zA-Z]+)(\d+)|([a-zA-Z]\d+)([a-zA-Z]+)|([a-zA-Z]{2,})(\d+)' )
    matches = p.finditer(token)
    ls = []
    for m in matches:
        l = len(m.groups()) + 1
        temp = [ m.group(i) for i in range(1,l) if m.group(i) != None ]
        #print( [ m.group(i) for i in range(1,l)] )
        ls.extend(temp)
    if len(ls) == 0:
        ls.append(token)
    
    return ls

def str_int_str_case_tokenizer(code):
    tokens = code.split()
    tokenized = []
    for token in tokens:
        tokenized.extend( tokenize_with_str_int_str(token) )
    return ' '.join(tokenized)




'''
case_sensitive ->  case sensitive
'''
def tokenize_with_snake_case(token):
    return token.split('_')

def snake_case_tokenizer(code):
    tokens = code.split()
    tokenized = []
    for token in tokens:
        tokenized.extend( tokenize_with_snake_case(token) )
    return ' '.join(tokenized)
 



'''
tradeBonus -> trade Bonus
qV -> qV
wMtrl -> w Mtrl
JComponentButton -> J Component Button
'''
def tokenize_with_camel_case(token):
    if len(token) <= 2:
        return [token]
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', token)
    return [m.group(0) for m in matches]

def camel_case_tokenizer(code):
    tokens = code.split()
    tokenized = []
    for token in tokens:
        tokenized.extend( tokenize_with_camel_case(token) )
    return ' '.join(tokenized)


'''
Remove all the characters which are non ascii
'''

def remove_non_ascii( code ):
    return code.encode("ascii", errors="ignore").decode()


'''
remove space, tab and newline
'''
def remove_escape_charaters( code ):
    return ' '.join( code.split() )


'''
helper function
get all literals and their type and method type
'''
def isSetter(func_name, total_token):
    if func_name == None:
        return False
    return func_name.startswith('set')

def isGetter(func_name, total_token):
    if func_name == None:
        return False
    return func_name.startswith('get')

def isTester(func_name, total_token):
    if func_name == None:
        return False
    return func_name.startswith('test')
    
    
def get_literals( code ):
    tokens = list(javalang.tokenizer.tokenize(code))
    literal_token = {}
    literal_token['int'] = []
    literal_token['float'] = []
    literal_token['bool'] = []
    literal_token['str'] = []
    for t in tokens:
        if isinstance(t, javalang.tokenizer.Integer) or  isinstance(t, javalang.tokenizer.DecimalInteger) or         isinstance(t, javalang.tokenizer.OctalInteger) or isinstance(t, javalang.tokenizer.BinaryInteger) or         isinstance(t, javalang.tokenizer.HexInteger):
            literal_token['int'].append(t.value)
        elif isinstance(t, javalang.tokenizer.FloatingPoint) or isinstance(t, javalang.tokenizer.DecimalFloatingPoint) or         isinstance(t, javalang.tokenizer.HexFloatingPoint):
            literal_token['float'].append(t.value)
        elif  isinstance(t, javalang.tokenizer.Character) or isinstance(t, javalang.tokenizer.String):
            literal_token['str'].append(t.value)
        elif isinstance(t, javalang.tokenizer.Boolean):
            literal_token['bool'].append(t.value)
    
    total_token = len(tokens)
    func_name = None
    for i in range(len(tokens)):
        if tokens[i].value == '(' and i > 0:
            func_name = tokens[i-1].value
            break
    
    return (literal_token, total_token, isSetter(func_name, total_token), isGetter(func_name, total_token), isTester(func_name, total_token))




'''
it tokenizes and removes comments, escape charaters
'''
def tokenize_and_remove_comments( code ):
    tokens = list(javalang.tokenizer.tokenize(code))
    ls = []
    for t in tokens:
        ls.append(t.value)
    return ' '.join(ls)




def code_filter(code):
    with open('code_filter_flag.json', 'r') as f:
        flags = json.load(f)
    
    if len(code.split()) < flags['delete_when_total_token_is_less_than']:
        return ''
    
    
    if len(code) > flags['maximum_code_length']:
        return ''
        
    literals, total_token, issetter, isgetter, istester = get_literals(code)
    
    if flags["remove_getter_methods"].lower() == 'true' and isgetter == True and total_token <= flags["maximum_token_for_getter_method"]:
        return ''
    
    if flags["remove_setter_methods"].lower() == 'true' and issetter == True and total_token <= flags["maximum_token_for_setter_method"]:
        return ''
    
    if flags["remove_tester_methods"].lower() == 'true' and istester == True and total_token <= flags["maximum_token_for_tester_method"]:
        return ''
    
    if flags['remove_non_ascii'].lower() == 'true':
        code = remove_non_ascii(code)
    
    if flags['tokenize and remove_comments'].lower() == 'true':
        code = tokenize_and_remove_comments(code)
    
    if flags['remove_escape_charaters'].lower() == 'true':
        code = remove_escape_charaters(code)
    
    if flags['replace_string_literal_with'].lower() != 'none':
        sl = literals['str']
        replacer = flags['replace_string_literal_with']
        for s in sl:
            code = code.replace(s, replacer)
            
    if flags['replace_int_literal_with'].lower() != 'none':
        sl = literals['int']
        replacer = flags['replace_int_literal_with']
        for s in sl:
            code = code.replace(s, replacer)
            
    if flags['replace_float_literal_with'].lower() != 'none':
        sl = literals['float']
        replacer = flags['replace_float_literal_with']
        for s in sl:
            code = code.replace(s, replacer)
            
    if flags['replace_bool_literal_with'].lower() != 'none':
        sl = literals['bool']
        replacer = flags['replace_bool_literal_with']
        for s in sl:
            code = code.replace(s, replacer)
    
    
    if flags['subtokenize_snake_case'].lower() == 'true':
        code = snake_case_tokenizer(code)
        
    
    if flags['subtokenize_camel_case'].lower() == 'true':
        code = camel_case_tokenizer(code)
        
        
    if flags['subtokenize_str_int_str'].lower() == 'true':
        code = str_int_str_case_tokenizer(code)
    
    
    
    
    return code


#print( code_filter('public void getFood ( int value ) { food Quantity = value + 1 + 2 + 3 + 3 + 3 + 4  + 3 + 5; }') )
