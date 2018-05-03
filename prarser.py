#hello

import string;

def getTests():
  found=True;
  i=1;
  while found:
    try:
      f = open(str(i)+".txt");
    except FileNotFoundError:
      return;
    yield f;
    i+=1;

t = getTests();
st= {};
line=1
col=1
errors = []
def lex(f):
  global st;
  global errors;
  st = f
  errors = []
  def serr(e):
    global errors;
    errors = errors + ["Error:" + e];
  def nextchar(*t):
    global st;
    
    while(st[0] == ' ' or st[0] == '\n'):
      st = st[1::]
    #print(t, st[0:5]);
    for c in t:
      if c == st[0]:
        st = st[1::]
        return True;

    return False;
  def gotochar(t, inc=True):
    global st;
    while(st[0] != t):
      #print(st[0], t)
      st = st[1::]
    if inc:
      st = st[1::]

  def next(t):
    global st;
    
    while(st[0] == ' ' or st[0] == '\n'):
      st = st[1::]
    #print(t, st[0]);
    i = 0;
    while(i < len(t)):
      #print(t[i], st[i]);
      if t[i] != st[i]:
          return False;
      i+=1;
    st = st[i::];
    return True;

  def special():
    return nextchar("+", "-", "*", "/", "\\", "^", "~", ":", ".", "?", " ", "#", "$", "&");
  def character():
    if alphanum():
      return 1;
    if special():
      return 1;
    return False;
  def strng():
    if character():
      strng();
    else:
      return False;
    
    return 1;
  def digit():
    return nextchar(*[str(i) for i in range(0, 10)]);
  def numeral():
    if digit():
      numeral();
    else:
      return False;
    
    return 1;
  def uppercase():
    return nextchar(*(string.ascii_uppercase+"_"));
  def lowercase():
    return nextchar(*string.ascii_lowercase);

  def alphanum():
    if lowercase():
      return True;
    if uppercase():
      return True;
    if digit():
      return True;
    return False;

  def charlist():
    if alphanum():
      charlist();

  def variable():
    if uppercase():
      charlist();
      return 1;

  def small_atom():
    if lowercase():
      charlist();
      return True;

    return False;


  def atom():
    if small_atom():
      return True;
    if nextchar('\'') and strng() and nextchar('\''):
      return True;

    return False;

  def structure():
    if nextchar("(") and term_list() and nextchar(")"):
      return 1;
    return False;

  def term():
    if atom():
      structure()
      return 1;
    if variable():
      return 1;
    if numeral():
      return 1;
    return False;

  def term_list():
    if term():
      if(nextchar(',')):
        term_list();
      return True;
    return False;    

  def predicate():
    if atom():
      if nextchar("("):
        term_list();
        if not nextchar(")"):
          serr("invalid term");
          gotochar(")");
      return 1;
    return False;
      

    

  def predicate_list():
    if not predicate():
      gotochar(",", False);
      serr("invalid predicate");

    if(nextchar(",")):
      predicate_list();

  def query():
    if(next("?- ")):
      predicate_list()

    if not nextchar("."):
      serr("Query must end with .")

  def clause():
    if(not predicate()):
      return False;

    if(next(":-")):
      predicate_list();

    nextchar(".");
    return True;


  def clause_list():
    
    if(clause()):
      clause_list();

  def program():
    clause_list();
    query();

  program();
  if not errors:
    print("Correct");
  else:
    print("Syntax Error:",*errors, sep='\n')



####
for f in t:
  s = f.read();
  lex(s)
  print("");
####