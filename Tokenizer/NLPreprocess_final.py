#Tanveer Muttaqueen
#tanveer.mutta@gmail.com



import re
import json
from bs4 import BeautifulSoup 

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
        ls.extend(temp)
    if len(ls) == 0:
        ls.append(token)
    
    return ls

def str_int_str_case_tokenizer(nl):
    tokens = nl.split()
    tokenized = []
    for token in tokens:
        tokenized.extend( tokenize_with_str_int_str(token) )
    return ' '.join(tokenized)


'''
case_sensitive ->  case sensitive
'''
def tokenize_with_snake_case(token):
    return token.split('_')

def snake_case_tokenizer(nl):
    tokens = nl.split()
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

def camel_case_tokenizer(nl):
    tokens = nl.split()
    tokenized = []
    for token in tokens:
        tokenized.extend( tokenize_with_camel_case(token) )
    return ' '.join(tokenized)


'''
Remove all the characters which are non ascii
'''
def remove_non_ascii( nl ):
    return nl.encode("ascii", errors="ignore").decode()


'''
remove space, tab and newline
'''
def remove_escape_charaters( nl ):
    return ' '.join( nl.split() )


'''
make nl lowercase
'''
def to_lowercase(nl):
    return nl.lower()


def remove_parameter_return_throws_info( nl, tokens ):
    for t in tokens:
        x = nl.find(t)
        if x != -1:
            nl = nl[:x]
    return nl



def remove_comment_tags(nl):
    nl = nl.replace('/*', '')
    nl = nl.replace('*/', '')
    nl = nl.replace('*', '')
    nl = nl.replace('//', '')
    return nl



def remove_unwanted_symbol(nl, unwanted):
    rep = ['link', 'code', 'inheritdoc', 'param', 'return', 'throws']
    for r in rep:
        nl = nl.replace( '@'+r, 'XX' + r )

    nl = ''.join( c for c in nl if not c in unwanted )
    
    for r in rep:
        nl = nl.replace( 'XX'+r, '@' + r )
    return nl



def tokenize_nl(nl):
    s = set([c for c in text if c.isalnum() == False and c != ' '])
    for c in s:
        nl = nl.replace( c, ' ' + c + ' ' )
    return nl
    

def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_html_tags(nl, html_tags ):
    nl = strip_html(nl)
    for tag in html_tags:
        nl = nl.replace( tag, ' ')
    return nl



def remove_at_words(nl, at_words):
    for w in at_words:
        nl = nl.replace(w, ' ')
    return nl



def minimum_alphabet_check(nl, cnt):
    letters = sum(c.isalpha() for c in nl)
    if letters < cnt:
        return ''
    return nl



def tokenize(nl):
    spchar = ['.', '-', '[', ']', '{', '}', '(', ')', '<', '>', '/', '\\', ',', ':', '\"', ';', '&', '@', '#', '!', '?', '+', '%', '*', '^', '~', '\'', '='   ]
    rspchar = [' . ', ' - ', ' [ ', ' ] ', ' { ', ' } ', ' ( ', ' ) ', ' < ', ' > ', ' / ', ' \\ ', ' , ', ' : ', ' \" ', ' ; ', ' & ', ' @ ', ' # ', ' ! ', ' ? ', ' + ', ' % ', ' * ', ' ^ ', ' ~ ', ' \' ', ' = '  ]
    for c, r in zip(spchar, rspchar):
        nl = nl.replace( c, r)
    return nl




def remove_begin_end_user_doc(nl):
    nl = nl.replace( '<!-- begin-user-doc -->', '' )
    nl = nl.replace( '<!-- end-user-doc -->', '' )
    return nl
    




def maximum_length_check(nl, cnt):
    if len(nl) > cnt:
        return ''
    return nl



def nl_filter(nl):
    with open('nl_filter_flag.json', 'r') as f:
        flags = json.load(f)
        
    if flags['subtokenize_snake_case'].lower() == 'true':
        nl = snake_case_tokenizer(nl)
    
    if flags['subtokenize_camel_case'].lower() == 'true':
        nl = camel_case_tokenizer(nl)
        
    if flags['subtokenize_str_int_str'].lower() == 'true':
        nl = str_int_str_case_tokenizer(nl)
    
    if flags['to_lower_case'].lower() == 'true':
        nl = to_lowercase(nl)
 
    if flags['remove_parameter_return_throws_info'].lower() == 'true':
        nl = remove_parameter_return_throws_info(nl, flags["_tokens_parameter_return_throws_info"] )
    
    if flags['remove_non_ascii'].lower() == 'true':
        nl = remove_non_ascii(nl)
    
    if flags['remove_html_tags'].lower() == 'true':
        nl = remove_html_tags(nl, flags["_tokens_html_tags"])
        
    if flags['remove_comment_tags'].lower() == 'true':
        nl = remove_comment_tags(nl)
    
    if flags['remove_at_words'].lower() == 'true':
        nl = remove_at_words(nl, flags["_tokens_at_words"])
    
    if flags['remove_unwanted_symbol'].lower() == 'true':
        nl = remove_unwanted_symbol(nl, flags["_tokens_unwanted_symbol"])
    
    if flags['tokenize'].lower() == 'true':
        nl = tokenize(nl)
        
    if flags['remove_begin_end_user_doc'].lower() == 'true':
        nl = remove_begin_end_user_doc(nl)
    
    if flags['remove_escape_charaters'].lower() == 'true':
        nl = remove_escape_charaters(nl)
        
    nl = minimum_alphabet_check(nl, flags['minimum_alphabet_count'] )
    
    nl = maximum_length_check(nl, flags['maximum_length'] )
    
    return nl



#print( nl_filter("hello <p> world123 ok_ok JGss aaBB {@link world} haha @return int") )

