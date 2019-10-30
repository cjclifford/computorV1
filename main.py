import sys
import math
import re

def main(equation):
    eq = Equation(equation)
    # try:
    eq.solve()
    # except Exception as error:
    #     print(error)

class Equation:
    def __init__(self, equation):
        self.lhs = Expression(equation.split('=')[0])
        self.rhs = Expression(equation.split('=')[1])
        self.__determine_highest_order()
        print('Polynomial degree:', self.__highest_order)

    def __determine_highest_order(self):
        self.__highest_order = 0
        for term in self.lhs.term_list + self.rhs.term_list:
            if term.exponent > self.__highest_order and term.coefficient != 0:
                self.__highest_order = term.exponent

    def solve(self):
        self.rhs.flip_polarity()

        for term in self.rhs.term_list:
            self.lhs.term_list.append(term)

        self.__simplify()
        self.__print_reduced()

        if self.__highest_order == 0:
            self.__solve_degree_0()
        elif self.__highest_order == 1:
            self.__solve_degree_1()
        elif self.__highest_order == 2:
            self.__solve_quadratic()
        else:
            raise Exception('Polynomial degree outside the range of 0 -> 2')

    def __simplify(self):
        simplified_term_list = []
        for i in range(0, self.__highest_order + 1):
            simplified_term = Term(0, i)
            for term in self.lhs.term_list:
                if term.exponent == i:
                    simplified_term.coefficient += term.coefficient
            simplified_term_list.append(simplified_term)
        self.lhs.term_list = simplified_term_list

    def __print_reduced(self):
        equation = []
        for i in range(len(self.lhs.term_list) - 1, -1, -1):
            term_str = 'Reduced form: '
            term_str += str(int(self.lhs.term_list[i].coefficient)) if int(self.lhs.term_list[i].coefficient) == self.lhs.term_list[i].coefficient else ''
            if self.lhs.term_list[i].exponent > 0:
                term_str += 'x^' + str(self.lhs.term_list[i].exponent)
            equation.append(term_str)
        print(' + '.join(equation) + ' = 0')

    def __solve_degree_0(self):
        print(self.lhs.term_list[0].coefficient == 0)

    def __solve_degree_1(self):
        print('x', '=', str(-self.lhs.term_list[0].coefficient / self.lhs.term_list[1].coefficient))
    
    def __solve_quadratic(self):
        # Quadratic Formula
        #              discriminant
        #               ----+----
        # x = (-b +/- √(b^2 - 4ac) ) / 2a

        a = self.lhs.term_list[2].coefficient
        b = self.lhs.term_list[1].coefficient
        c = self.lhs.term_list[0].coefficient

        discriminant = b ** 2 - (4 * a * c)

        if discriminant < 0:
            raise Exception('Discriminant is strictly negative. No solution possible.')
            
        else:
            print('Discriminant is strictly positive, the solutions are:')

        discriminant_sqrt = math.sqrt(discriminant)
        denominator = 2 * a

        plus = (-b + discriminant_sqrt) / denominator
        minus = (-b - discriminant_sqrt) / denominator

        print('x', '=', plus)
        if minus != plus:
            print('x', '=', minus)


class Expression:
    def __init__(self, expression):
        self.expression = ''.join(expression.split())
        self.term_list = []
        self.__parse_expression()

    def __parse_expression(self):
        self.term_list = [self.__parse_term(term) for term in re.findall('([+-]*(?:(?:(?:\d+(?:\.\d*)?|\.?\d+)?\*?[a-z]\^\d+)|(?:(?:\d+(?:\.\d*)?|\.?\d+)\*?[a-z])|(?:(?:\d+(?:\.\d*)?|\.?\d+)|(?:[a-z]))))', self.expression)]

    def flip_polarity(self):
        for term in self.term_list:
            term.coefficient *= -1

    def __parse_term(self, term):
        print(term)
        polarity = 1
        indeterminate = ''
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
                indeterminate = c
            elif c.isdigit():
                if prev_term_was_circumflex:
                    exponent_str += c
                else:
                    coefficient_str += c
            elif c == '.':
                coefficient_str += c

        coefficient = polarity * float(coefficient_str) if coefficient_str != '' else 1
        exponent = 0 if not term_has_indeterminate else int(exponent_str) if exponent_str != '' else 1
        print(coefficient)
        return Term(coefficient, exponent)

class Term:
    def __init__(self, coefficient, exponent):
        if int(coefficient) == coefficient:
            self.coefficient = int(coefficient)
        else:
            self.coefficient = coefficient
        self.exponent = exponent

    def __str__(self):
        return str((self.coefficient, self.exponent))

if __name__ == "__main__":
    main(sys.argv[1])