import sys
import math
import re

def main(equation):
    eq = Equation(equation)
    try:
        eq.solve()
    except PolynomialDegreeTooHighException as error:
        print(error)
    except NegativeDiscriminantException as error:
        print(error)
    except InvalidPolynomialException as error:
        print(error)
    except MultipleIndeterminatesException as error:
        print(error)

class Equation:
    def __init__(self, equation):
        self.lhs = Expression(equation.split('=')[0])
        self.rhs = Expression(equation.split('=')[1])
        self.__determine_highest_order()
        self.__determine_indeterminates(equation)
        print('Polynomial degree:', self.__highest_order)

    def __determine_highest_order(self):
        self.__highest_order = 0
        for term in self.lhs.terms + self.rhs.terms:
            if term.exponent > self.__highest_order and term.coefficient != 0:
                self.__highest_order = term.exponent

    def __determine_indeterminates(self, equation):
        self.__indeterminates = []
        for c in equation:
            if c.isalpha() and not self.__indeterminates.__contains__(c):
                self.__indeterminates.append(c)

    def solve(self):
        if len(self.__indeterminates) > 1:
            raise MultipleIndeterminatesException('Cannot solve polynomials with multiple indeterminates')

        self.rhs.flip_polarity()

        for term in self.rhs.terms:
            self.lhs.terms.append(term)

        self.__simplify()
        self.__print_reduced()

        if self.__highest_order not in range(0, 3):
            raise PolynomialDegreeTooHighException('Cannot solve polynomials of degree higher than 2')

        if self.__highest_order == 0:
            self.__solve_degree_0()
        elif self.__highest_order == 1:
            self.__solve_degree_1()
        elif self.__highest_order == 2:
            self.__solve_quadratic()

    def __simplify(self):
        simplified_terms = []
        for i in range(0, self.__highest_order + 1):
            simplified_term = Term(0, i)
            for term in self.lhs.terms:
                if term.exponent == i:
                    simplified_term.coefficient += term.coefficient
            simplified_terms.append(simplified_term)
        simplified_terms.reverse()
        self.lhs.terms = simplified_terms

    def __print_reduced(self):
        equation = []
        for term in self.lhs.terms:
            term_str = ''
            if term.coefficient == 0:
                continue
            elif int(term.coefficient) == term.coefficient:
                term_str += str(int(term.coefficient))
            else:
                term_str += str(term.coefficient)
            if term.exponent > 0:
                term_str += self.__indeterminates[0]
                if term.exponent > 1:
                    term_str += '^' + str(term.exponent)
            equation.append(term_str)
        print('Reduced form: ', ' + '.join(equation) + ' = 0')

    def __solve_degree_0(self):
        print(self.lhs.terms[0].coefficient == 0)

    def __solve_degree_1(self):
        print('x', '=', str(-self.lhs.terms[0].coefficient / self.lhs.terms[1].coefficient))
    
    def __solve_quadratic(self):
        # Quadratic Formula:
        #
        #           discriminant
        #            ┌───┴────┐
        # x = (-b ± √(b² - 4ac)) / 2a

        a = self.lhs.terms[0].coefficient
        b = self.lhs.terms[1].coefficient
        c = self.lhs.terms[2].coefficient

        discriminant = b ** 2 - (4 * a * c)

        if discriminant < 0:
            raise NegativeDiscriminantException('Discriminant is strictly negative. No solution possible.')
            
        else:
            print('Solution' + ('s:' if discriminant != 0 else ':'))

        discriminant_sqrt = math.sqrt(discriminant)
        denominator = 2 * a

        plus = (-b + discriminant_sqrt) / denominator
        print(self.__indeterminates[0], '=', int(plus) if int(plus) == plus else plus)

        if discriminant != 0:
            minus = (-b - discriminant_sqrt) / denominator
            print(self.__indeterminates[0], '=', int(minus) if int(minus) == minus else minus)

class Expression:
    def __init__(self, expression):
        self.expression = ''.join(expression.split())
        self.terms = []
        self.__parse_expression()

    def __parse_expression(self):
        self.terms = [self.__parse_term(term) for term in re.findall('([+-]*(?:(?:(?:\d+(?:\.\d*)?|\.?\d+)?\*?[a-z]\^\d+)|(?:(?:\d+(?:\.\d*)?|\.?\d+)\*?[a-z])|(?:(?:\d+(?:\.\d*)?|\.?\d+)|(?:[a-z]))))', self.expression)]

    def flip_polarity(self):
        for term in self.terms:
            term.coefficient *= -1

    def __parse_term(self, term):
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

class NegativeDiscriminantException(Exception):
    pass

class PolynomialDegreeTooHighException(Exception):
    pass

class InvalidPolynomialException(Exception):
    pass

class MultipleIndeterminatesException(Exception):
    pass

if __name__ == "__main__":
    main(sys.argv[1])