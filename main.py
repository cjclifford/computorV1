import sys

def main(equation):
    eq = Equation(equation)
    # eq.solve()

class Equation:
    def __init__(self, equation):
        self.lhs = Expression(equation.split('=')[0])
        self.rhs = Expression(equation.split('=')[1])
        self.rhs.flip_polarity()
        for term in self.rhs.term_list:
            self.lhs.term_list.append(term)

    def solve(self):
        self.__simplify()
        for term in self.lhs.term_list:
            print(term)

    def __simplify(self):
        simplified_term_list = []
        for i in range(0, 3):
            simplified_term = Term(0, i)
            for term in self.lhs.term_list:
                if term.exponent == i:
                    simplified_term.coefficient += term.coefficient
            simplified_term_list.append(simplified_term)
        self.lhs.term_list = simplified_term_list

class Expression:
    def __init__(self, expression):
        self.expression = ''.join(expression.split())
        self.term_list = []
        self.__parse_expression()

    def __parse_expression(self):
        new_term = []
        prev_char_was_term = False
        terms = []
        for c in self.expression:
            if c in ('+', '-'):
                if prev_char_was_term:
                    prev_char_was_term = False
                    terms.append(new_term)
                    new_term = [c]
                else:
                    new_term.append(c)
            else:
                prev_char_was_term = True
                new_term.append(c)
        if len(new_term) > 0:
            terms.append(new_term)
        for term in terms:
            self.term_list.append(self.__parse_term(term))
        for term in self.term_list:
            print(term)

    def flip_polarity(self):
        for term in self.term_list:
            term.coefficient *= -1

    def __parse_term(self, term):
        polarity = 1
        coefficient_str = ''
        exponent_str = ''
        prev_term_was_circumflex = False
        term_has_indeterminate = False
        for c in term:
            if c == '-':
                polarity *= -1
            elif c == '^':
                prev_term_was_circumflex = True
            elif c.isalpha():
                term_has_indeterminate = True
                self.indeterminate = c
            elif c.isdigit():
                if prev_term_was_circumflex:
                    exponent_str += c
                else:
                    coefficient_str += c
            else:
                pass
        coefficient = polarity * int(coefficient_str) if coefficient_str is not '' else 1
        exponent = 0 if not term_has_indeterminate else int(exponent_str) if exponent_str is not '' else 1
        return Term(coefficient, exponent)

class Term:
    def __init__(self, coefficient, exponent):
        self.coefficient = coefficient
        self.exponent = exponent
    
    def __str__(self):
        return str((self.coefficient, self.exponent))

if __name__ == "__main__":
    main(sys.argv[1])