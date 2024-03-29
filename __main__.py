from cmp.core.lexer.scanner import build_lexer, tokenizer
from cmp.core.parser.parser import parse

tests = [
    "42",
    "print(42);",
    "print((((1 + 2) * 3) * 4) / 5);",
    "print(sin(2 * PI) * 2 + cos(3 * PI / log(4, 64)));",
    """ let a = 0, c = 2 in
        let b = 1 , x =2+5-(3*9) in {
            print(a);
            print(b);
        };
    """,
    """
     let a = "hola mundo" in while(a<3){ a:=a+6; }
    """,
    """
     let a = "hola mundo" in
         let b = a:= c :=8in while(a<3){ a:=a+6; }
    """,
    """
     let o:Point =new Point(8,8) in {
        if (o.x < o.y)  45;
        while (o.length() < 5){
          o := o+1;
          for (a in iterable){
              if ((a<o) | ((o.x^8)>=5 & o.length()+2 <= 3 ) & !a ==40 ){
                o:=0;
              };
              o := a - o;
          };
        };
     }
    """,
    """
      print("hello world")
    """,
    """
    {
      print(a@"hola")
      print(a@@"hola")
      print(a@@a)
      print(a@@a.length())
      print(a.length()@@a.length())
      print(a.length()@@a.x)
      print("hello world");
    }  
    """,
    """
let pt = new Point() in
    print("x: " @ pt.getX() @ "; y: " @ pt.getY());
""",
    """
    function tan(x) => sin(x) / cos(x)
    function cot(x) => 1 / tan(x)
    function tan(x) => sin(x) / cos(x)

     function operate(x, y) {
    print(x + y);
    print(x - y);
    print(x * y);
    print(x / y);
}
    type Point {
    x = 0;
    y = 0;

    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x[0] := x;
    setY(y) => self.y[int(sin(self.y))] := y;
}

    """,
    """
type Knight inherits Person {
    name() => "Sir" @@ base();
}
    """,
    """
type Person(firstname, lastname) {
    firstname = firstname;
    lastname = lastname;

    name() => self.firstname @@ self.lastname;
}
    """,
    """
type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) {
    length()=> phi*rho + (cos(rho))/(sen(phi));
}
""",
"""
protocol Hashable {
    hash(): Number;
}
""",
"""
protocol Equatable extends Hashable {
    equals(other: Object): Boolean;
}
""",
"""
let a = [1,2,3,4] in for (x in a ){
  print(a);
}
"""

    # """
    # (5.5 + 0.5) * 2 - 34 /2;
    # let x: Number in (let y = 5 in x + y);
    # let x = 1 > 3, y = 7 < 8 in (x & y == (true | false)); 
    # """
]


if __name__ == '__main__':
    lexer = build_lexer()
    
    for t in tests:
        print(f'Parsing:\n{t}\n\n')
        
        code_tokens = tokenizer(t, lexer=lexer)
        print([t.lex for t in code_tokens])
        print([t.token_type for t in code_tokens])
        right_most_parse = parse(code_tokens)
        print(right_most_parse)
        print(f'Code {t} parsed successfully!!\n\n\n')
        print('------------------------------------------')




