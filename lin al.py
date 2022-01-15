class Matrix:
    """
    class of matrices
    """
    def __init__(self, matrix: list):
        self.mat_list = matrix
    
    def matrix(self):
        """
        checks if the input is a matrix
        """
        try:
            row_len = len(self.mat_list[0])
        except IndexError:
            return False

        for row in self.mat_list:
            if len(row) != row_len or row_len == 0:
                return False
        return True

    def _square(self):
        """
        checks if the matrix is
        a square matrix
        """
        col_len = len(self.mat_list)
        try:
            row_len = len(self.mat_list[0])
        except IndexError:
            return False

        index = 1

        if not self.matrix():
            return False
        else:
            if col_len == row_len:
                return True
            return False

    def _constructor(self, removed_col: int):
        '''
        constructs the minor of the
        matrix with the first row and removed_col
        removed from the original matrix
        ''' 
        mat_list_copy = []
        for e in self.mat_list:
            mat_list_copy.append(list(tuple(e)))
        # creats new inner lists
        # disconnected from the
        # inner lists of the initial list
        input_dim = len(self.mat_list)
        out = []
        index = 1
        # starts from one b/c the
        # the first row is removed
        removed_col = removed_col - 1
        # pyhton index starts from 0

        while index < input_dim:
            mat_list_copy[index].pop(removed_col)
            out.append(mat_list_copy[index])
            index += 1
        return Matrix(out)

    def det(self):
        """
        matrix determinant calculator
        """
        if not self._square():
            return 0
        # non-square matrices have det = 0
        if len(self.mat_list) == 2:
            return self.mat_list[0][0]*self.mat_list[1][1] - self.mat_list[0][1]*self.mat_list[1][0]

        else:
            det_mat = 0
            index = 0
            while index < len(self.mat_list[0]):
                det_mat += (-1)**(1 + (index + 1))*self.mat_list[0][index]* \
                        self._constructor(index + 1).det()
                index += 1
            return det_mat

    def __str__(self):
        """
        prints the matrix, if it's a matrix

        example:

        matrix = Matrix( [ ['a', 'b'], ['c', 'd'] ] )

        print(matrix)

        | a b |
        | c d |
        """
        if not self.matrix():
            return 'NOT A MATRIX'

        # finds the longest string (number) entree
        # in the matrix
        maxim = len(str(self.mat_list[0][0]))
        for e in self.mat_list:
            for i in e:
                if len(str(i)) > maxim:
                    maxim = len(str(i))

        out = ''
        for row in self.mat_list:
            part_out = '|'
            index = 0
            while index < len(row):
                part_out += f'{(1 + (maxim-len(str(row[index]))))*" "}{row[index]}'
                index += 1
            part_out += ' |\n' 
            out += part_out
        return out[:-1]

    def transpose(self):
        """
        returns the transpose of the
        input matrix and empty list if it's
        not a valid matrix
        """
        if not self.matrix():
            return 'NOT A MATRIX'
        trans_out = []
        trans_col_len = len(self.mat_list[0])
        trans_row_len = len(self.mat_list)

        index_col = 0
        

        while index_col < trans_col_len:
            row = []
            index_row = 0
            while index_row < trans_row_len:
                row.append(self.mat_list[index_row][index_col])
                index_row += 1

            index_col += 1
            trans_out.append(row)

        return Matrix(trans_out)

    def mult(self, other):
        """
        computes the product of two matrices
        self is the outter matrix
        """
        if not self.matrix() and not other.matrix(): 
            return "BOTH MATRICES WRONG"
        else:
            if not self.matrix():
                return "FIRST MATRIX WRONG"
            elif not other.matrix():
                return "SECOND MATRIX WRONG"

        scnd_matrix_trans = other.transpose()
        if len(self.mat_list[0]) != len(scnd_matrix_trans.mat_list[0]):
            return "MISMATCHED MATRIX DIMENSIONS"

        matrix_out = []

        for row1 in self.mat_list:
            row_out = []

            for row2 in scnd_matrix_trans.mat_list:
                entree_index = 0
                entree_out_val = 0
                while entree_index < len(row2):
                    entree_out_val += row1[entree_index]*row2[entree_index]
                    entree_index += 1
                row_out.append(entree_out_val)
            matrix_out.append(row_out)

        return Matrix(matrix_out)

    def _vector_to_poly(self):

        if not self.matrix() or len(self.mat_list[0]) > 1:
            return 'NOT A VECTOR'

        vect = self.transpose().mat_list
        deg_coef_pairs = {}
        for i in range(len(vect[0])):
            if vect[0][i] != 0:
                deg_coef_pairs[i] = vect[0][i]

        poly = ''
        for deg in deg_coef_pairs:
            if '0' == str(deg_coef_pairs[deg])[-1]:
                coeff = int(deg_coef_pairs[deg])
            else:
                coeff = deg_coef_pairs[deg]
            if deg > 0:
                if coeff >= 0:
                    poly = f'+{coeff}x^{deg}' + poly if coeff != 1 else f'+x^{deg}' + poly
                else:
                    poly = f'{coeff}x^{deg}' + poly if coeff != -1 else f'-x^{deg}' + poly
            else:
                poly = f'+{coeff}' + poly if coeff >= 0 else f'{coeff}' + poly
        if not len(poly) == 0:
            return poly[1:] if poly[0] == '+' else poly
        else: return '0'

class Poly:
    """
    polynomial function class
    the only possible input
    variable is x
    
    p(x) = a_n*x^n + .... + a_1*x^1 + a_0
    is the only valid form 
    """
    def __init__(self, poly):
        self.poly = poly
    

    def _separator(self):
        """
        splits poly into terms
        """
        poly = self.poly[:]
        ind = 0
        while ind < len(poly):
            if poly[ind] == '-' and ind != 0:
                poly = poly[: ind] + '+' + poly[ind:]
                ind += 1
            ind += 1
        return poly.split('+')

    def degree(self, in_list=None):
        """
        returns the degree of the polynmial regardless
        if the input is a list or str (however for
        it to give a list, it requres self to be a polynimial
        given that the list contains the terms of the input
        polynimial (self))
        """
        terms = self._separator() if in_list is None else in_list

        largest_term = terms[0]

        degree = int(largest_term[largest_term.index("^")+1:]) \
                                if '^' in largest_term else None
        if degree is None:
            if "x" in largest_term:
                degree = 1
            else:
                degree = 0
        return degree
    
    def coeffs(self):
        """
        returns the coefficients of the polynimial
        from the highest degree to the lowerst
        """
        
        out_list = []
        for ement in self._separator():
            if 'x' in ement and '-x' not in ement and ement[0] != 'x':
                out_list.append(float(ement[:ement.index('x')]))
            elif '-x' in ement or ement[0] == 'x':
                if '-x' in ement:
                    out_list.append(float(-1))
                else:
                    out_list.append(float(1))
            else:
                out_list.append(float(ement))

        return out_list

    def _poly_into_vect(self):
        degree_list = []
        degree_list.append(self.degree())
        ind = 1
        while ind < len(self._separator()):
            degree_list.insert(0, self.degree(self._separator()[ind:]))
            ind += 1

        vector = []
        coeffs = self.coeffs()
        coeffs.reverse()
        deg_coef_pairs = dict(zip(degree_list, coeffs))

        for i in range(degree_list[-1] + 1):
            if i not in deg_coef_pairs:
                vector.append(0)
            else:
                vector.append(deg_coef_pairs[i])
        return Matrix([vector]).transpose()

    def poly_der(self, nth=1):

        """
        computes the derivative
        of a polynomial using linear albegra
        1. converts poly (str) into a vector
        2. creates the diffferentiation matrix
        3. pluggs the poly vector into the matrix
        4. converts back to str
        """
        mat_size = self.degree() + 1
        mat_list = []

        for i in range(mat_size):
            mat_list.append([0]*mat_size)
            mat_list[i-1][i] = i
        
        der_matrix = Matrix(mat_list)
        same_but_composite_matrix = Matrix(mat_list)

        for _ in range(nth-1):
            # nth-1 bc it's not really
            # the number of derivatives
            # aka the number of matrices
            #but the number of matrix compositions
            der_matrix = der_matrix.mult(same_but_composite_matrix)

        out_poly_as_vect = der_matrix.mult(self._poly_into_vect())

        return out_poly_as_vect._vector_to_poly()


class polyTree:
    """
    a class of polynomials of the form
    p(x) = a_n*x^n + .... + a_1*x^1 + a_0
    no factorized forms
    """
    def __init__(self, root, sublist):
        self.root = root
        self.sublist = sublist

    def der(self):
        """
        computes the derivative of p(x) [p'(x)]

        the function is very input sensative and
        will eihter crash or return an incorrect output
        if the format is wrong.

        sidenote:

        the function also accepts second derivative
        requests (by func.der().der()) since it
        returns in a function-friendly format

        1. addition has at least 2 trees in its sublist

        2. multiplication has 2 (no more, no less) trees in
        its sublist where the left one (sublist[0]) is
        always a number and the right one (sublist[1]) is
        either ^ or x or

        3. exponentiation has only 2 trees where the
        left one is the variable and the right one is a number

        4. the function (tree) is not empty

        some forbidden -> permitted formats
        1. x^2 -> 1*x^2
        2. x^2*2 -> 2*x^2
        3. a_0*x^0 -> a_0

        example:

        expo1 = polyTree("^", [polyTree("x", []), polyTree(3, [])])
        mult1 = polyTree("*", [polyTree(-3, []), expo1])

        expo2 = polyTree("^", [polyTree("x", []), polyTree(2, [])])
        mult2 = polyTree("*", [polyTree(-1, []), expo2])

        mult3 = polyTree("*", [polyTree(1, []), polyTree("x", [])])

        num1 = polyTree(1, [])

        func = polyTree("+", [mult1, mult2, mult3, num1])

        p(x) = -3*x^3 + (-1)*x^2 +1*x + 1

        func.der()

        p'(x) = -9*x^2 + (-2)*x + 1 + 0
        """
        if isinstance(self.root, (int, float)):
            return polyTree(0, [])
        else:
            
            if self.root == "+":
                derivative = polyTree("+", [])
                for ement in self.sublist:
                        derivative.sublist.append(ement.der())
                return derivative

            elif self.root == "*":
                no_expo = True
                # checks if it will have to multiple
                # scalar of x by the exponent

                if self.sublist[1].root == "^":
                    no_expo = False

                if no_expo:
                    return self.sublist[0]
                
                # the else is the exponentiation
                else:
                    scalar = self.sublist[0].root
                    expo = self.sublist[1].sublist[1].root
                    return polyTree("*", [polyTree(scalar*expo, []),
                                         self.sublist[1].der()])
            # the else is the exponentiation
            else:
                exponent = self.sublist[1].root-1
                if exponent != 1:
                    return polyTree("^", [self.sublist[0],
                                         polyTree(exponent, [])])
                else:
                    return self.sublist[0]

# matrix = Matrix( [ [5, 6, 6, 8], [2, 2, 2, 8], [6, 6, 2, 8], [2, 3, 6, 7] ] )
# print(matrix)
# print(matrix.transpose())

pol= Poly('-2x^5+4x-1')
print(pol.poly_der())