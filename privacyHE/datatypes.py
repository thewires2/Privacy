from typing import List

from seal import Ciphertext, Plaintext

import privacyHE


class EncryptedValue:
    def __init__(self, value):
        if isinstance(value, EncryptedValue): value = value._ciphertext
        if not isinstance(value, Ciphertext):
            value = privacyHE.encrypt(value)._ciphertext

        self._ciphertext = value
        self._mode = privacyHE._mode

    @property
    def _is_float(self):
        return self._mode['type'] == 'float'


    def _binop(
        self, other,
        cipher_func, plain_func = None,
        _is_mult: bool = False
    ):
        if isinstance(other, EncryptedValue):
            other = other._ciphertext

        # Must normalize floats to same scale before adding/subtracting
        evaluator = privacyHE._evaluator

        # If adding, we need to match scale and modulus
        if self._is_float:
            target_scale = privacyHE._mode['default_scale']
            if not _is_mult:
                self._ciphertext.scale(target_scale)

            parms = self._ciphertext.parms_id()
            def normalize(x, p=parms):
                privacyHE._evaluator.mod_switch_to_inplace(x, p)


        # After each multiplication, we should relinearize
        def renormalize(x):
            if _is_mult:
                evaluator.relinearize_inplace(x, privacyHE._relin_keys)
                if self._is_float:
                        evaluator.rescale_to_next_inplace(x)

            # Determine type of other operand
        if not isinstance(other, Ciphertext):
            from privacyHE.encryptors import encode_item
            if plain_func is not None:
                # Use plain_func for performance
                pt = encode_item(other)
                if self._is_float: normalize(pt)
                result = plain_func(self._ciphertext, pt)
                renormalize(result)
                return EncryptedValue(result)
            else:
                # Fallback to encrypting and using cipher_func
                other = privacyHE.encrypt(other)._ciphertext

        # If adding, we need to match scale and modulus
        #if self._is_float and not _is_mult:
        if self._is_float:
            other.scale(target_scale)
            try:
                normalize(other)
            except:
                self._ciphertext.scale(target_scale)
                normalize(self._ciphertext, p=other.parms_id())


        # Compute binary operation
        result = cipher_func(self._ciphertext, other)

        renormalize(result)
        return EncryptedValue(result)


    # Arithmetic
    def __add__(self, other):
        return self._binop(
            other,
            privacyHE._evaluator.add,
            privacyHE._evaluator.add_plain
        )



    def __sub__(self, other):
        return self._binop(
            other,
            privacyHE._evaluator.sub,
            privacyHE._evaluator.sub_plain
        )


    def __mul__(self, other):
        return self._binop(
            other,
            privacyHE._evaluator.multiply,
            privacyHE._evaluator.multiply_plain,
            _is_mult = True
        )

    def __neg__(self):
        return 0 - self

    __radd__ = __add__
    __rmul__ = __mul__
    def __rsub__(self, other):
        return EncryptedValue(other) - self


    def __truediv__(self, other):
        if not self._is_float:
            raise NotImplementedError('Integer division is not implemented!')
        if isinstance(other, int) or isinstance(other, float):
            return self * (1/other)
        else:
            raise NotImplementedError('Only division by an unencrypted value is implemented!')

    def square(self):
        evaluator = privacyHE._evaluator
        output = evaluator.square(self._ciphertext)
        evaluator.relinearize_inplace(output, privacyHE._relin_keys)
        if self._is_float:
            evaluator.rescale_to_next_inplace(output)
        return EncryptedValue(output)


    def __pow__(self, other):
        if isinstance(other, int) and other >= 0:
            # Exponentiation by squaring
            components = []
            curr = self
            bits = bin(other)[:1:-1]
            for i, digit in enumerate(bits):
                if digit == '1':
                    components.append(curr)
                if i < len(bits) - 1:
                    curr = curr.square()
            return smart_product(components)
        else:
            if self._is_float:
                raise NotImplementedError('Fractional powers not yet implemented')
            else:
                raise TypeError('Only non-negative, unencrypted integer exponents are supported in integer mode!')

    def __repr__(self):
        type_string = self._mode['type']
        return f'<encrypted {type_string}>'


    def save(self, filepath: str):
        """Saves this encrypted value to the given file."""
        self._ciphertext.save(filepath)


def load_encrypted_value(filepath: str) -> EncryptedValue:
    """Loads a saved encrypted value from the given file."""
    ciphertext = Ciphertext()
    ciphertext.load(privacyHE._context, filepath)
    return EncryptedValue(ciphertext)


# Return the product of the given list.
# A smart algorithm is used to conserve the noise budget.
def smart_product(values: List[EncryptedValue]) -> EncryptedValue:
    if not values: return privacyHE.encrypt(1)
    if len(values) == 1: return values[0]

    new = []
    for i in range(len(values) // 2):
        new.append(values[2*i] * values[2*i+1])
    if len(values) % 2 == 1:
        new.append(values[-1])
    return smart_product(new)
