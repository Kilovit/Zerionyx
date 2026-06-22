# Python Code Extraction - Zerionyx
Generated on: 2026-06-22 16:20:26

## File: `src\__init__.py`
```python
from .interp import INFO, Fore, Style, run
```

## File: `src\consts.py`
```python
import os
import string

DIGITS = string.digits
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
INFO = "v5.0.5 (2025-10-05 07:48:30)"
LIBS_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_STRING = "STRING"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_FLOORDIV = "FLOORDIV"
TT_POW = "POW"
TT_MOD = "MOD"
TT_EQ = "EQ"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LSQUARE = "LSQUARE"
TT_RSQUARE = "RSQUARE"
TT_EE = "EE"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"
TT_COMMA = "COMMA"
TT_ARROW = "ARROW"
TT_NEWLINE = "NEWLINE"
TT_DOT = "DOT"
TT_LBRACE = "LBRACE"
TT_RBRACE = "RBRACE"
TT_EOF = "EOF"
TT_COLON = "COLON"
TT_DOLLAR = "DOLLAR"
TT_AND = "AND"
TT_DOUBLE_STAR = "DSTAR"
TT_PLUSEQ = "PLUSEQ"
TT_MINUSEQ = "MINUSEQ"
TT_MULEQ = "MULEQ"
TT_DIVEQ = "DIVEQ"
TT_FLOORDIVEQ = "FLOORDIVEQ"
TT_MODEQ = "MODEQ"
TT_POWEQ = "POWEQ"
KEYWORDS = [
    "and",
    "or",
    "not",
    "if",
    "elif",
    "else",
    "for",
    "to",
    "do",
    "step",
    "while",
    "defun",
    "done",
    "return",
    "continue",
    "break",
    "load",
    "in",
    "del",
    "namespace",
    "using",
]
```

## File: `src\datatypes.py`
```python
import operator
from concurrent.futures import Future as PyFuture
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from queue import Queue as PyQueue

from .errors import MError, RTError, TError
from .utils import RTResult


class ThreadPoolError(Exception):
    def __init__(self, err):
        self.err = err
        super().__init__(err)


class Context:

    __slots__ = (
        "display_name",
        "parent",
        "parent_entry_pos",
        "symbol_table",
        "private_symbol_table",
        "using_vars",
        "nonlocal_vars",
        "escaped",
        "locals_stack",
    )

    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None
        self.private_symbol_table = None
        self.using_vars = set()
        self.nonlocal_vars = set()
        self.escaped = False
        self.locals_stack = None


class SymbolTable:

    __slots__ = ("symbols", "parent")

    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def change(self, other):
        self.symbols = other.symbols
        self.parent = other.parent

    def remove(self, name):
        del self.symbols[name]

    def exists(self, value):
        return True if value in self.symbols.values() else False

    def copy(self):
        return SymbolTable().change(self)


class Object:
    __slots__ = ("fields", "pos_start", "pos_end", "context")

    def __init__(self):
        self.set_pos()
        self.set_context()
        self.fields = []

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def type(self):
        return "Object"

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def dollared_by(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def moduled_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def execute(self, _, __):
        return RTResult().failure(
            self.illegal_operation(error_str="Can't call non-function")
        )

    def copy(self):
        raise Exception("No copy method defined")

    def is_true(self):
        return False

    def prequaled_by(self, other: "Object"):
        return None, self.illegal_operation(other)

    def get(self, other):
        return self.illegal_operation(other)

    def iter(self):
        return None, self.illegal_operation(
            error_str="Iteration is not supported for this type"
        )

    def illegal_operation(self, other=None, error_str=None):
        if not other:
            other = self
        return TError(
            self.pos_start,
            other.pos_end,
            f'Illegal operation -> {error_str or "unknown"}',
            self.context,
        )


class Channel(Object):
    __slots__ = ("queue",)

    def __init__(self, queue_instance=None):
        super().__init__()
        self.queue = queue_instance if queue_instance else PyQueue()

    def copy(self):
        return self

    def type(self):
        return "<channel>"

    def __repr__(self):
        return f"<channel size={self.queue.qsize()}>"


class ThreadWrapper(Object):
    __slots__ = "thread"

    def __init__(self, thread):
        super().__init__()
        self.thread = thread

    def copy(self):
        copy = ThreadWrapper(self.thread)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def type(self):
        return "<thread>"

    def __str__(self):
        return f"<thread id={self.thread.ident} active={self.thread.is_alive()}>"

    def __repr__(self):
        return self.__str__()

    def join(self, timeout=None):
        return self.thread.join(timeout)

    def is_alive(self):
        return self.thread.is_alive()

    def cancel(self):
        if self.thread.is_alive():
            self.thread._stop()

    def type(self):
        return "<thread>"


class NoneObject(Object):

    __slots__ = "value"

    def __init__(self, value):
        super().__init__()
        self.value = value

    def copy(self):
        copy = NoneObject(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return False

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self):
        return str(self.value).lower()

    def type(self):
        return "<none>"

    def get_comparison_eq(self, other):
        if isinstance(other, NoneObject):
            return Number.true.set_context(self.context), None
        return Number.false.set_context(self.context), None

    def get_comparison_ne(self, other):
        if isinstance(other, NoneObject):
            return Number.false.set_context(self.context), None
        return Number.true.set_context(self.context), None

    def notted(self):
        return Number.true.set_context(self.context)

    def anded_by(self, other):
        if not isinstance(other, NoneObject) and not isinstance(other, Bool):
            return None, None
        return Bool(self.value and other.value).set_context(self.context), None

    def ored_by(self, other):
        if not isinstance(other, NoneObject) and not isinstance(other, Bool):
            return None, None
        return Bool(self.value or other.value).set_context(self.context), None


NoneObject.none = NoneObject("none")


class Bool(Object):
    __slots__ = ("value",)

    def __init__(self, value):
        super().__init__()
        self.value = bool(value)

    def copy(self):
        copy = Bool(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value

    def type(self):
        return "<bool>"

    def notted(self):
        return Bool(not self.value).set_context(self.context), None

    def anded_by(self, other):
        if not isinstance(other, Bool):
            return None, None
        return Bool(self.value and other.value).set_context(self.context), None

    def ored_by(self, other):
        if not isinstance(other, Bool):
            return None, None
        return Bool(self.value or other.value).set_context(self.context), None

    def _get_comparison_result(self, other, op):
        if (
            isinstance(other, Bool)
            and not isinstance(self, NoneObject)
            and not isinstance(other, NoneObject)
        ):
            result = bool(op(self.value, other.value))
            return Bool(result).set_context(self.context), None

        if isinstance(self, NoneObject):
            if isinstance(other, NoneObject):
                result = op in (operator.eq, operator.le, operator.ge)
            else:
                result = op is operator.ne
            return Bool(result).set_context(self.context), None

        return Bool(op is operator.ne).set_context(self.context), None

    def get_comparison_eq(self, other):
        return self._get_comparison_result(other, operator.eq)

    def get_comparison_ne(self, other):
        return self._get_comparison_result(other, operator.ne)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self):
        return str(self.value).lower()


Bool.true = Bool(True)
Bool.false = Bool(False)


class CFloat(Object):
    __slots__ = ("value", "context", "pos_start", "pos_end", "fields")

    def __init__(self, value, context=None, pos_start=None, pos_end=None):
        if isinstance(value, Fraction):
            self.value = value
        else:
            self.value = Fraction(str(value))

        self.context = context
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.fields = []

    def set_context(self, context=None):
        self.context = context
        return self

    def copy(self):
        return CFloat(self.value, self.context, self.pos_start, self.pos_end)

    def _convert_to_fraction(self, other):
        if isinstance(other, CFloat):
            return other.value
        if isinstance(other, Number):
            if isinstance(other.value, int):
                return Fraction(other.value)
            try:
                return Fraction(str(other.value))
            except (ValueError, ZeroDivisionError, TypeError):
                return None
        return None

    def added_to(self, other):
        other_frac = self._convert_to_fraction(other)
        if other_frac is not None:
            result = self.value + other_frac
            return CFloat(result).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't add cfloat to '{other.type()}'"
        )

    def subbed_by(self, other):
        other_frac = self._convert_to_fraction(other)
        if other_frac is not None:
            result = self.value - other_frac
            return CFloat(result).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't subtract cfloat from '{other.type()}'"
        )

    def multed_by(self, other):
        other_frac = self._convert_to_fraction(other)
        if other_frac is not None:
            result = self.value * other_frac
            return CFloat(result).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't multiply cfloat by '{other.type()}'"
        )

    def dived_by(self, other):
        other_frac = self._convert_to_fraction(other)
        if other_frac is not None:
            if other_frac == 0:
                return None, RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )
            result = self.value / other_frac
            return CFloat(result).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't divide cfloat by '{other.type()}'"
        )

    def moduled_by(self, other):
        other_frac = self._convert_to_fraction(other)
        if other_frac is not None:
            if other_frac == 0:
                return None, RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )
            result = self.value % other_frac
            return CFloat(result).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't mod cfloat by '{other.type()}'"
        )

    def powed_by(self, other):
        other_frac = self._convert_to_fraction(other)
        if other_frac is not None:
            try:
                result = self.value**other_frac
                if isinstance(result, complex):
                    return None, MError(
                        self.pos_start,
                        self.pos_end,
                        "Math domain error (imaginary numbers are not supported)",
                        self.context,
                    )
                return CFloat(result).set_context(self.context), None
            except (ValueError, OverflowError, ZeroDivisionError):
                return None, MError(
                    self.pos_start,
                    self.pos_end,
                    "Math domain error",
                    self.context,
                )
        return None, Object.illegal_operation(
            other, f"Can't power cfloat by '{other.type()}'"
        )

    def floordived_by(self, other):
        other_frac = self._convert_to_fraction(other)
        if other_frac is not None:
            if other_frac == 0:
                return None, MError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )
            result = self.value // other_frac
            return Number(int(result)).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't floor divide cfloat by '{other.type()}'"
        )

    def _get_comparison_result(self, other, op):
        other_frac = self._convert_to_fraction(other)
        if other_frac is not None and not isinstance(self, NoneObject):
            return Bool(op(self.value, other_frac)).set_context(self.context), None

        if isinstance(self, NoneObject):
            is_none_other = isinstance(other, NoneObject)
            if op == operator.eq:
                return Bool(is_none_other).set_context(self.context), None
            if op == operator.ne:
                return Bool(not is_none_other).set_context(self.context), None

        return None, Object.illegal_operation(
            other, f"Can't compare cfloat with '{other.type()}'"
        )

    def get_comparison_eq(self, other):
        return self._get_comparison_result(other, operator.eq)

    def get_comparison_ne(self, other):
        return self._get_comparison_result(other, operator.ne)

    def get_comparison_lt(self, other):
        return self._get_comparison_result(other, operator.lt)

    def get_comparison_gt(self, other):
        return self._get_comparison_result(other, operator.gt)

    def get_comparison_lte(self, other):
        return self._get_comparison_result(other, operator.le)

    def get_comparison_gte(self, other):
        return self._get_comparison_result(other, operator.ge)

    def anded_by(self, other):
        if not isinstance(other, (Number, CFloat)):
            return None, Object.illegal_operation(
                other, f"Can't perform logical AND on cfloat and '{other.type()}'"
            )
        return Bool(self.is_true() and other.is_true()).set_context(self.context), None

    def ored_by(self, other):
        if not isinstance(other, (Number, CFloat)):
            return None, Object.illegal_operation(
                other, f"Can't perform logical OR on cfloat and '{other.type()}'"
            )
        return Bool(self.is_true() or other.is_true()).set_context(self.context), None

    def notted(self):
        return Bool(not self.is_true()).set_context(self.context), None

    def is_true(self):
        return self.value != 0 if not isinstance(self, NoneObject) else False

    def type(self):
        return "<cfloat>"

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if isinstance(self, NoneObject):
            return "none"
        if self.value.denominator == 1:
            return str(self.value.numerator)
        return str(float(self.value))


class Number(Object):
    __slots__ = ("value", "context", "pos_start", "pos_end", "fields")

    def __init__(self, value, context=None, pos_start=None, pos_end=None):
        self.value = value
        self.context = context
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.fields = []

    def set_context(self, context=None):
        self.context = context
        return self

    def copy(self):
        return Number(self.value, self.context, self.pos_start, self.pos_end)

    def _convert_value(self, other):
        if isinstance(other, Number):
            return other.value
        elif isinstance(other, CFloat):
            return float(other.value)
        return None

    def added_to(self, other):
        other_value = self._convert_value(other)
        if other_value is not None:
            return Number(self.value + other_value).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't add number to '{other.type()}'"
        )

    def subbed_by(self, other):
        other_value = self._convert_value(other)
        if other_value is not None:
            return Number(self.value - other_value).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't subtract number from '{other.type()}'"
        )

    def multed_by(self, other):
        other_value = self._convert_value(other)
        if other_value is not None:
            return Number(self.value * other_value).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't multiply number by '{other.type()}'"
        )

    def dived_by(self, other):
        other_value = self._convert_value(other)
        if other_value is not None:
            if other_value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )
            return Number(self.value / other_value).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't divide number by '{other.type()}'"
        )

    def moduled_by(self, other):
        other_value = self._convert_value(other)
        if other_value is not None:
            if other_value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )
            return Number(self.value % other_value).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't mod number by '{other.type()}'"
        )

    def powed_by(self, other):
        other_value = self._convert_value(other)
        if other_value is not None:
            try:
                result = self.value**other_value
                if isinstance(result, complex):
                    return None, MError(
                        self.pos_start,
                        self.pos_end,
                        "Math domain error (imaginary numbers are not supported)",
                        self.context,
                    )
                return Number(result).set_context(self.context), None
            except (ValueError, OverflowError, ZeroDivisionError):
                return None, MError(
                    self.pos_start, self.pos_end, "Math domain error", self.context
                )
        return None, Object.illegal_operation(
            other, f"Can't power number by '{other.type()}'"
        )

    def floordived_by(self, other):
        other_value = self._convert_value(other)
        if other_value is not None:
            if other_value == 0:
                return None, MError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )
            return Number(self.value // other_value).set_context(self.context), None
        return None, Object.illegal_operation(
            other, f"Can't floor divide number by '{other.type()}'"
        )

    def _get_comparison_result(self, other, op):
        other_value = self._convert_value(other)
        if other_value is not None and not isinstance(self, NoneObject):
            return Bool(op(self.value, other_value)).set_context(self.context), None
        if isinstance(self, NoneObject):
            if isinstance(other, NoneObject):
                result = op in (operator.eq, operator.le, operator.ge)
            else:
                result = op is operator.ne
            return Bool(result).set_context(self.context), None
        return Bool(op is operator.ne).set_context(self.context), None

    def get_comparison_eq(self, other):
        return self._get_comparison_result(other, operator.eq)

    def get_comparison_ne(self, other):
        return self._get_comparison_result(other, operator.ne)

    def get_comparison_lt(self, other):
        return self._get_comparison_result(other, operator.lt)

    def get_comparison_gt(self, other):
        return self._get_comparison_result(other, operator.gt)

    def get_comparison_lte(self, other):
        return self._get_comparison_result(other, operator.le)

    def get_comparison_gte(self, other):
        return self._get_comparison_result(other, operator.ge)

    def anded_by(self, other):
        if not isinstance(other, (Number, CFloat)):
            return None, Object.illegal_operation(
                other, f"Can't perform logical AND on number and '{other.type()}'"
            )
        if isinstance(self, NoneObject) or isinstance(other, NoneObject):
            return None, TError(
                self.pos_start,
                self.pos_end,
                "Can't perform logical operation with 'none'",
                self.context,
            )
        return (
            Bool((self.value != 0) and (other.value != 0)).set_context(self.context),
            None,
        )

    def ored_by(self, other):
        if not isinstance(other, (Number, CFloat)):
            return None, Object.illegal_operation(
                other, f"Can't perform logical OR on number and '{other.type()}'"
            )
        if isinstance(self, NoneObject) or isinstance(other, NoneObject):
            return None, TError(
                self.pos_start,
                self.pos_end,
                "Can't perform logical operation with 'none'",
                self.context,
            )
        return (
            Bool((self.value != 0) or (other.value != 0)).set_context(self.context),
            None,
        )

    def notted(self):
        if isinstance(self, NoneObject):
            return None, TError(
                self.pos_start,
                self.pos_end,
                "Can't perform logical operation with 'none'",
                self.context,
            )
        return Bool(not bool(self.value)).set_context(self.context), None

    def is_true(self):
        return bool(self.value) if not isinstance(self, NoneObject) else False

    def type(self):
        if isinstance(self.value, int):
            return "<int>"
        elif isinstance(self.value, float):
            return "<float>"
        elif isinstance(self, NoneObject):
            return "<none>"

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if isinstance(self, NoneObject):
            return "none"
        if isinstance(self.value, bool):
            return "true" if self.value else "false"
        s = str(self.value)
        if "e" in s or "E" in s:
            return s.replace("e", "*10^(").replace("E", "*10^(") + ")"
        return s


Number.false = Bool.false
Number.true = Bool.true
Number.none = NoneObject.none


class String(Object):
    __slots__ = "value"

    def __init__(self, value):
        super().__init__()
        self.value = value
        self.fields = ["size"]

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(
                other, f"Can't add string to '{other.type()}'"
            )

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(
                other, f"Can't multiply string by '{other.type()}'"
            )

    def _make_comparison(self, other, op, type_to_check):
        if isinstance(other, type_to_check):
            result = bool(op(self.value, other.value))
            return Bool(result).set_context(self.context), None
        default_result = True if op is operator.ne else False
        return Bool(default_result).set_context(self.context), None

    def get_comparison_eq(self, other):
        return self._make_comparison(other, operator.eq, String)

    def get_comparison_ne(self, other):
        return self._make_comparison(other, operator.ne, String)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def type(self):
        return "<str>"

    def __str__(self):
        return self.value

    def dollared_by(self, index):
        if not isinstance(index, Number):
            return None, self.illegal_operation(index, "Index must be a number")
        try:
            return String(self.value[index.value]), None
        except IndexError:
            return None, RTError(
                index.pos_start,
                index.pos_end,
                f"Index {index.value} is out of bounds for string of size {len(self.value)}",
                self.context,
            )

    def iter(self):
        return iter([String(ch) for ch in self.value]), None

    def __repr__(self):
        return repr(self.value)


class PyObject(Object):
    __slots__ = "value"

    def __init__(self, obj):
        super().__init__()
        self.value = obj

    def get_obj(self):
        return self.value

    def copy(self):
        c = PyObject(self.value)
        c.set_pos(self.pos_start, self.pos_end)
        c.set_context(self.context)
        return c

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self):
        return f"<py-obj {self.value}>"

    def type(self):
        return "<py-obj>"


class List(Object):

    __slots__ = "value"

    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        new_list = self.copy()
        new_list.value.append(other)
        return new_list, None

    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.value.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    f"Index {other.value} is out of bounds for list of size {len(self.value)}",
                    self.context,
                )
        else:
            return None, self.illegal_operation(
                other, f"Can't subtract list by '{other.type()}'"
            )

    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.value.extend(other.value)
            return new_list, None
        elif isinstance(other, Number):
            new_list = self.copy()
            new_list.value = self.value * other.value
            return new_list, None
        else:
            return None, self.illegal_operation(
                other, f"Can't multiply list by '{other.type()}'"
            )

    def dollared_by(self, other):
        if isinstance(other, Number):
            try:
                return self.value[other.value], None
            except IndexError:
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    f"Index {other.value} is out of bounds for list of size {len(self.value)}",
                    self.context,
                )
        else:
            return None, self.illegal_operation(other, "Index must be a number")

    def copy(self):
        copy = List(self.value[:])
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def get_comparison_eq(self, other):
        if not isinstance(other, List):
            return Number.false.set_context(self.context), None
        if len(self.value) != len(other.value):
            return Number.false.set_context(self.context), None

        for i in range(len(self.value)):
            cmp, err = self.value[i].get_comparison_eq(other.value[i])
            if err:
                return None, err
            if not cmp.is_true():
                return Number.false.set_context(self.context), None
        return Number.true.set_context(self.context), None

    def get_comparison_ne(self, other):
        eq_result, _ = self.get_comparison_eq(other)
        if eq_result == Number.true:
            return Number.false.set_context(self.context), None
        return Number.true.set_context(self.context), None

    def is_true(self):
        return len(self.value) > 0

    def type(self):
        return "<list>"

    def iter(self):
        return iter(self.value), None

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return str(self.value)


class HashMap(Object):
    __slots__ = "value"

    def __init__(self, value):
        super().__init__()
        self.value: dict[str, Object] = {}
        if isinstance(value, HashMap):
            raw = value.value
        elif isinstance(value, dict):
            raw = value
        else:
            raw = {}

        for k, v in raw.items():
            key_str = str(k)
            self.value[key_str] = v

    def is_true(self):
        return len(self.value) > 0

    def added_to(self, other):
        if not isinstance(other, HashMap):
            return None, self.illegal_operation(other)

        new_map_value = self.value.copy()
        for key, value in other.value.items():
            new_map_value[key] = value

        return HashMap(new_map_value), None

    def type(self):
        return "<hashmap>"

    def dollared_by(self, index):
        if not isinstance(index, String):
            return None, self.illegal_operation(index)

        try:
            return self.value[index.value], None
        except KeyError:
            return None, RTError(
                index.pos_start,
                index.pos_end,
                "Key not found in hashmap",
                self.context,
            )

    def get_index(self, index):
        if not isinstance(index, String):
            return None, self.illegal_operation(index)
        try:
            return self.value[index.value], None
        except KeyError:
            return None, RTError(
                index.pos_start,
                index.pos_end,
                "Key not found in hashmap",
                self.context,
            )

    def set_index(self, index, value):
        if not isinstance(index, String):
            return None, self.illegal_operation(index)
        new_value = self.value.copy()
        new_value[index.value] = value
        return HashMap(new_value)

    def iter(self):
        pairs = [List([String(str(k)), v]) for k, v in self.value.items()]
        return iter(pairs), None

    def get_comparison_eq(self, other):
        if not isinstance(other, HashMap):
            return Number.false.set_context(self.context), None
        if len(self.value) != len(other.value):
            return Number.false.set_context(self.context), None

        for key, value in self.value.items():
            if key not in other.value:
                return Number.false.set_context(self.context), None
            cmp, err = value.get_comparison_eq(other.value[key])
            if err:
                return None, err
            if not cmp.is_true():
                return Number.false.set_context(self.context), None
        return Number.true.set_context(self.context), None

    def get_comparison_ne(self, other):
        eq_result, _ = self.get_comparison_eq(other)
        if eq_result == Number.true:
            return Number.false.set_context(self.context), None
        return Number.true.set_context(self.context), None

    def __len__(self) -> int:
        return len(self.value)

    def copy(self):
        copied_map = HashMap(self.value.copy())
        copied_map.set_pos(self.pos_start, self.pos_end)
        copied_map.set_context(self.context)
        return copied_map

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return str(self.value)


class File(Object):

    __slots__ = ("name", "path")

    def __init__(self, name, path):
        super().__init__()
        self.name = name
        self.path = path

    def _make_comparison(self, other, op, type_to_check):
        if isinstance(other, type_to_check):
            result = bool(op(self.path, other.path))
            return Bool(result).set_context(self.context), None
        default_result = True if op is operator.ne else False
        return Bool(default_result).set_context(self.context), None

    def get_comparison_eq(self, other):
        return self._make_comparison(other, operator.eq, File)

    def get_comparison_ne(self, other):
        return self._make_comparison(other, operator.ne, File)

    def copy(self):
        copy = File(self.name, self.path)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def type(self):
        return "<file>"

    def __repr__(self):
        return f"<file {self.name}>"


class NameSpace(Object):
    __slots__ = ("name", "value", "_internal")

    def __init__(self, name):
        super().__init__()
        self.name = name

        self.value = HashMap({})

        self._internal = {
            "context_": Number.none,
            "statements_": Number.none,
            "initialized_": Number.false,
        }

    def get(self, name, checked=False):
        if name in self._internal and checked:
            return self._internal[name]

        r, err = self.value.dollared_by(String(name))
        if err:
            return None
        return r

    def set(self, name, value, checked=False):
        if name in self._internal and checked:
            self._internal[name] = value
        else:
            self.value = self.value.set_index(String(name), value)
        return self

    def copy(self):
        copied_ns = NameSpace(self.name)
        copied_ns.value = self.value.copy()
        copied_ns._internal = self._internal.copy()
        copied_ns.set_pos(self.pos_start, self.pos_end)
        copied_ns.set_context(self.context)
        return copied_ns

    def type(self):
        return "<namespace>"

    def __repr__(self):
        return f"<namespace {self.name}>"


class Bytes(Object):
    __slots__ = ("value",)

    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Bytes):
            return Bytes(self.value + other.value).set_context(self.context), None
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        if isinstance(other, Bytes):
            return Bool(self.value == other.value).set_context(self.context), None
        return Number.false.set_context(self.context), None

    def get_comparison_ne(self, other):
        if isinstance(other, Bytes):
            return Bool(self.value != other.value).set_context(self.context), None
        return Number.true.set_context(self.context), None

    def dollared_by(self, index):
        if not isinstance(index, Number):
            return None, self.illegal_operation(index)
        try:
            return Number(self.value[index.value]).set_context(self.context), None
        except IndexError:
            return None, RTError(
                index.pos_start,
                index.pos_end,
                f"Index {index.value} is out of bounds for bytes of size {len(self.value)}",
                self.context,
            )

    def copy(self):
        copy = Bytes(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def iter(self):
        pairs = [Number(i) for i in self.value]
        return iter(pairs), None

    def is_true(self):
        return len(self.value) > 0

    def type(self):
        return "<bytes>"

    def __str__(self):
        return self.value.hex()

    def __repr__(self):
        return self.value.hex()


class ThreadPool(Object):
    __slots__ = ("executor",)

    def __init__(self, max_workers):
        super().__init__()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def copy(self):
        return self

    def type(self):
        return "<thread-pool>"

    def __repr__(self):
        return f"<thread-pool max_workers={self.executor._max_workers}>"


class Future(Object):
    __slots__ = ("future",)

    def __init__(self, future: PyFuture):
        super().__init__()
        self.future = future

    def copy(self):
        return self

    def type(self):
        return "<future>"

    def __repr__(self):
        return f"<future state={self.future._state}>"
```

## File: `src\errors.py`
```python
from colorama import Fore, Style, init

init(autoreset=True, strip=False)


def get_line_from_text(text, line_number):
    if not text:
        return None
    lines = text.split("\n")
    if 0 <= line_number < len(lines):
        return lines[line_number]
    return None


def create_traceback_header(error_name, total_width=75):
    line1 = "-" * total_width + "\n"
    traceback_str = "Traceback (most recent call last)"
    remaining_space = total_width - len(error_name)
    line2 = f"{error_name}{traceback_str:>{remaining_space}}\n"
    return line1 + line2


class Error:
    __slots__ = ["pos_start", "pos_end", "error_name", "details"]

    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def __str__(self):
        result = create_traceback_header(self.error_name)

        result += f'  File {Fore.MAGENTA}"{self.pos_start.fn}"{Style.RESET_ALL}, line {Fore.MAGENTA}{self.pos_start.ln + 1}{Style.RESET_ALL}\n'

        line_text = get_line_from_text(self.pos_start.ftxt, self.pos_start.ln)

        if line_text is not None:
            result += f"{Fore.LIGHTRED_EX}--> {line_text.strip()}{Style.RESET_ALL}\n"

        result += f"\n{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{self.error_name}{Style.RESET_ALL}: {Fore.MAGENTA}{self.details}{Style.RESET_ALL}"
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "IllegalCharacterError", details)


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "ExpectedCharacterError", details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start, pos_end, "InvalidSyntaxError", details)


class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, "RuntimeError", details)
        self.context = context

    def generate_traceback_frames(self):
        frames = []
        ctx = self.context
        pos = self.pos_start
        while ctx:
            if pos:
                frames.append({"pos": pos, "display_name": ctx.display_name})
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        return list(reversed(frames))

    def __str__(self):
        result = create_traceback_header(self.error_name)
        frames = self.generate_traceback_frames()

        for frame in frames:
            pos = frame["pos"]
            display_name = frame["display_name"]

            result += f'  File {Fore.MAGENTA}"{pos.fn}"{Style.RESET_ALL}, line {Fore.MAGENTA}{pos.ln + 1}{Style.RESET_ALL}, in {Fore.MAGENTA}{display_name}{Style.RESET_ALL}\n'

        line_text = get_line_from_text(self.pos_start.ftxt, self.pos_start.ln)
        if line_text is not None:
            result += f"{Fore.LIGHTRED_EX}--> {line_text.strip()}{Style.RESET_ALL}\n"

        result += f"\n{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{self.error_name}{Style.RESET_ALL}: {Fore.MAGENTA}{self.details}{Style.RESET_ALL}"
        return result


class MError(RTError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context)
        self.error_name = "MathError"


class IError(RTError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context)
        self.error_name = "IOError"


class TError(RTError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context)
        self.error_name = "TypeError"
```

## File: `src\interp.py`
```python
import csv
import hashlib
import json
import math
import os
import platform
import random
import re
import socket
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
import zlib
from copy import deepcopy
from datetime import date, datetime, timedelta
from getpass import getpass
from shutil import copy, rmtree
from threading import Thread
from urllib.parse import unquote

from colorama import Fore, Style, init

from .consts import *
from .datatypes import *
from .errors import Error, IError, MError, RTError, TError
from .lexer import Lexer
from .nodes import *
from .parser import *
from .utils import RTResult

init()
ssl._create_default_https_context = ssl._create_unverified_context
sys.setrecursionlimit(10000000)
BUILTIN_FUNCTIONS = []
global_symbol_table = SymbolTable()


module_cache = {}


def load_module(fn, interpreter):
    ast = None
    mtime = os.path.getmtime(fn)

    if fn in module_cache:
        cached_ast, error, cached_mtime = module_cache[fn]
        if mtime == cached_mtime:
            if error:
                return None, error
            ast = cached_ast
        else:
            ast = None

    if ast is None:
        with open(fn, "r", encoding="utf-8") as f:
            text = f.read()

        text_lines = text.splitlines()
        for i in range(len(text_lines)):
            text_lines[i] = text_lines[i].strip()

        lexer = Lexer(fn, "\n".join(text_lines))
        tokens, error = lexer.make_tokens()
        if error:
            return None, error

        parser = Parser(tokens)
        ast = parser.parse()

        module_cache[fn] = (ast, ast.error, mtime)

        if ast.error:
            return None, ast.error

    try:
        module_context = Context("<module>")
        module_context.symbol_table = global_symbol_table
        module_context.private_symbol_table = SymbolTable()
        module_context.private_symbol_table.set("is_main", Number.false)

        compiler = ASTCompiler()
        compiled_ast = compiler.compile(ast.node)
        result = interpreter.visit(compiled_ast, module_context)

        result.value = "" if str(result.value) == "none" else result.value
        return result.value, result.error
    except KeyboardInterrupt:
        print(
            "\n---------------------------------------------------------------------------"
        )
        print(
            "InterruptError                            Traceback (most recent call last)\n"
        )
        print(
            f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}InterruptError{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}User Terminated{Fore.RESET}{Style.RESET_ALL}"
        )
        sys.exit(2)


class FramePool:
    def __init__(self):
        self.context_pool = []
        self.table_pool = []

    def acquire_context(self, display_name, parent=None, parent_entry_pos=None):
        if self.context_pool:
            ctx = self.context_pool.pop()
            ctx.display_name = display_name
            ctx.parent = parent
            ctx.parent_entry_pos = parent_entry_pos
            ctx.symbol_table = None
            ctx.private_symbol_table = None
            ctx.using_vars.clear()
            ctx.nonlocal_vars.clear()
            ctx.escaped = False
            ctx.locals_stack = None
            return ctx
        return Context(display_name, parent, parent_entry_pos)

    def acquire_symbol_table(self, parent=None):
        if self.table_pool:
            table = self.table_pool.pop()
            table.symbols.clear()
            table.parent = parent
            return table
        return SymbolTable(parent)

    def release_context(self, ctx):
        if ctx is None:
            return
        if len(self.context_pool) < 2000:
            if ctx.symbol_table:
                self.release_symbol_table(ctx.symbol_table)
            if ctx.private_symbol_table:
                self.release_symbol_table(ctx.private_symbol_table)
            ctx.symbol_table = None
            ctx.private_symbol_table = None
            ctx.locals_stack = None
            self.context_pool.append(ctx)

    def release_symbol_table(self, table):
        if table is None:
            return
        if len(self.table_pool) < 4000:
            table.symbols.clear()
            table.parent = None
            self.table_pool.append(table)


global_frame_pool = FramePool()


class BaseFunction(Object):
    __slots__ = "name"

    def __init__(self, name):
        super().__init__()
        self.name = name or "?"

    def set_context(self, context=None):
        if hasattr(self, "context") and self.context:
            return self
        res = super().set_context(context)
        if context:
            context.escaped = True
        return res

    def generate_new_context(self, num_locals=0):
        new_context = global_frame_pool.acquire_context(
            self.name, self.context, self.pos_start
        )
        new_context.locals_stack = [Number.none] * num_locals
        new_context.symbol_table = global_frame_pool.acquire_symbol_table(
            new_context.parent.symbol_table if new_context.parent else None
        )
        new_context.private_symbol_table = global_frame_pool.acquire_symbol_table(
            new_context.parent.private_symbol_table if new_context.parent else None
        )
        return new_context

    def handle_arguments(
        self,
        param_names,
        defaults,
        vargs_name,
        kargs_name,
        positional_args,
        keyword_args,
        exec_ctx,
    ):
        res = RTResult()
        interpreter = Interpreter()
        if not vargs_name and len(positional_args) > len(param_names):
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Function takes {len(param_names)} positional arguments but {len(positional_args)} were given",
                    exec_ctx,
                )
            )

        for i, param_name in enumerate(param_names):
            if i < len(positional_args):
                exec_ctx.symbol_table.set(param_name, positional_args[i])
            elif param_name in keyword_args:
                exec_ctx.symbol_table.set(param_name, keyword_args.pop(param_name))
            else:
                default_value = defaults[i]
                if default_value is None:
                    return res.failure(
                        RTError(
                            self.pos_start,
                            self.pos_end,
                            f"Missing required argument '{param_name}'",
                            exec_ctx,
                        )
                    )

                is_node = not isinstance(default_value, Object)
                if is_node:
                    evaluated_default = res.register(
                        interpreter.visit(default_value, exec_ctx)
                    )
                    if res.should_return():
                        return res
                    exec_ctx.symbol_table.set(param_name, evaluated_default)
                else:
                    exec_ctx.symbol_table.set(param_name, default_value)

        if vargs_name:
            remaining_pos_args = positional_args[len(param_names) :]
            vargs_list = List(remaining_pos_args)
            exec_ctx.symbol_table.set(vargs_name, vargs_list.set_context(exec_ctx))

        if kargs_name:
            kargs_map = HashMap(keyword_args)
            exec_ctx.symbol_table.set(kargs_name, kargs_map.set_context(exec_ctx))
        elif keyword_args:
            first_unknown = next(iter(keyword_args.keys()))
            return res.failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Function got an unexpected keyword argument '{first_unknown}'",
                    exec_ctx,
                )
            )

        return res.success(None)


class Function(BaseFunction):
    def __init__(
        self,
        name,
        body_node,
        arg_names,
        defaults,
        vargs_name_tok,
        kargs_name_tok,
        should_auto_return,
        num_locals=0,
    ):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.defaults = defaults
        self.vargs_name = vargs_name_tok.value if vargs_name_tok else None
        self.kargs_name = kargs_name_tok.value if kargs_name_tok else None
        self.should_auto_return = should_auto_return
        self.num_locals = num_locals

    def execute(self, positional_args, keyword_args):
        res = RTResult()
        exec_ctx = self.generate_new_context(self.num_locals)

        if (
            not self.vargs_name
            and not self.kargs_name
            and not keyword_args
            and len(positional_args) == len(self.arg_names)
        ):
            for i, param_name in enumerate(self.arg_names):
                exec_ctx.locals_stack[i] = positional_args[i]
        else:
            res.register(
                self.handle_arguments(
                    self.arg_names,
                    self.defaults,
                    self.vargs_name,
                    self.kargs_name,
                    positional_args,
                    keyword_args,
                    exec_ctx,
                )
            )
            if res.should_return():
                if not exec_ctx.escaped:
                    global_frame_pool.release_context(exec_ctx)
                return res

        interpreter = Interpreter()
        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value is None:
            if not exec_ctx.escaped:
                global_frame_pool.release_context(exec_ctx)
            return res
        ret_value = (
            (value if self.should_auto_return else None)
            or res.func_return_value
            or Number.none
        )

        if not exec_ctx.escaped:
            global_frame_pool.release_context(exec_ctx)
        return res.success(ret_value)

    def copy(self):
        copy = Function(
            self.name,
            self.body_node,
            self.arg_names,
            self.defaults,
            Token(TT_IDENTIFIER, self.vargs_name) if self.vargs_name else None,
            Token(TT_IDENTIFIER, self.kargs_name) if self.kargs_name else None,
            self.should_auto_return,
            self.num_locals,
        )
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"

    def type(self):
        return "<func>"


class BuiltInFunction(BaseFunction):
    __slots__ = ("name", "body_node", "arg_names", "defaults", "should_auto_return")

    def __init__(self, name):
        super().__init__(name)

    def execute(self, positional_args, keyword_args):
        res = RTResult()
        exec_ctx = self.generate_new_context()
        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_execute_method)
        res.register(
            self.handle_arguments(
                param_names=method.arg_names,
                defaults=method.defaults,
                vargs_name=getattr(method, "vargs_name", None),
                kargs_name=None,
                positional_args=positional_args,
                keyword_args=keyword_args,
                exec_ctx=exec_ctx,
            )
        )
        if res.should_return():
            return res
        return_value = res.register(method(exec_ctx))
        if res.should_return():
            return res

        return res.success(return_value)

    def no_execute_method(self, _, __):
        raise Exception(f"No execute_{self.name} method defined")

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    @staticmethod
    def set_args(arg_names, defaults=None, vargs_name=None):
        if defaults is None:
            defaults = [None] * len(arg_names)

        def _args(f):
            f.arg_names = arg_names
            f.defaults = defaults
            f.vargs_name = vargs_name
            return f

        return _args

    @set_args(["value"], [String("")])
    def execute_println(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        if isinstance(value, String):
            print(value.value, flush=True)
            return RTResult().success(Number.none)
        print(repr(exec_ctx.symbol_table.get("value")), flush=True)
        return RTResult().success(Number.none)

    @set_args(["value"], [String("")])
    def execute_print(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        if isinstance(value, String):
            print(value.value, end="", flush=True)
            return RTResult().success(Number.none)
        print(repr(exec_ctx.symbol_table.get("value")), end="", flush=True)
        return RTResult().success(Number.none)

    @set_args(["prompt"], [String("")])
    def execute_input(self, exec_ctx):
        prompt = exec_ctx.symbol_table.get("prompt")
        text = input(prompt.value)
        return RTResult().success(String(text))

    @set_args(["prompt"], [String("")])
    def execute_get_password(self, exec_ctx):
        prompt = exec_ctx.symbol_table.get("prompt")
        pass_ = getpass(prompt.value)
        return RTResult().success(String(pass_))

    @set_args([])
    def execute_clear(self, _):
        os.system("cls" if os.name == "nt" else "clear")
        return RTResult().success(Number.none)

    @set_args(["value"])
    def execute_type(self, exec_ctx):
        data = exec_ctx.symbol_table.get("value")
        return RTResult().success(String(data.type()))

    @set_args(["value"])
    def execute_is_none(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        return RTResult().success(
            Number.true if isinstance(value, NoneObject) else Number.false
        )

    @set_args(["value"])
    def execute_is_num(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)

    @set_args(["value"])
    def execute_is_bool(self, exec_ctx):
        is_bool = isinstance(exec_ctx.symbol_table.get("value"), Bool)
        return RTResult().success(Number.true if is_bool else Number.false)

    @set_args(["value"])
    def execute_is_str(self, exec_ctx):
        is_str = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number.true if is_str else Number.false)

    @set_args(["value"])
    def execute_is_list(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number.true if is_number else Number.false)

    @set_args(["value"])
    def execute_is_func(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Number.true if is_number else Number.false)

    @set_args(["value", "reverse"], [None, Number.false])
    def execute_sort_fp(self, exec_ctx):
        lst = exec_ctx.symbol_table.get("value")
        reverse = exec_ctx.symbol_table.get("reverse")
        if not isinstance(lst, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'sort' must be a list",
                    exec_ctx,
                )
            )
        if not isinstance(reverse, Bool):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'sort' must be a boolean",
                    exec_ctx,
                )
            )

        if int(reverse.value) == 1:
            lst.value.sort(key=lambda x: x.value, reverse=True)
        elif int(reverse.value) == 0:
            lst.value.sort(key=lambda x: x.value)
        else:
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'sort' must be a boolean",
                    exec_ctx,
                )
            )
        return RTResult().success(lst)

    @set_args(["object", "value"])
    def execute_append(self, exec_ctx):
        obj_ = exec_ctx.symbol_table.get("object")
        value = exec_ctx.symbol_table.get("value")

        if isinstance(obj_, List):
            obj_.value.append(value)
            return RTResult().success(value)
        else:
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'append' must be a list",
                    exec_ctx,
                )
            )

    @set_args(["list", "index"])
    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")
        if not isinstance(list_, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'pop' must be a list",
                    exec_ctx,
                )
            )
        if not isinstance(index, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'pop' must be a number",
                    exec_ctx,
                )
            )
        try:
            element = list_.value.pop(int(index.value))
        except:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Element at this index could not be removed from list because index is out of bounds",
                    exec_ctx,
                )
            )
        return RTResult().success(element)

    @set_args(["listA", "listB"])
    def execute_extend(self, exec_ctx: Context):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")
        if not isinstance(listA, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'extend' must be a list",
                    exec_ctx,
                )
            )
        if not isinstance(listB, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'extend' must be a list",
                    exec_ctx,
                )
            )
        listA.value.extend(listB.value)
        return RTResult().success(Number.none)

    @set_args(["list", "index", "element"])
    def execute_insert(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list_")
        element = exec_ctx.symbol_table.get("element")
        index = exec_ctx.symbol_table.get("index")
        if not isinstance(list_, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'insert' must be a list",
                    exec_ctx,
                )
            )
        if not isinstance(index, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'insert' must be a number",
                    exec_ctx,
                )
            )
        list_.value.insert(int(index.value), element)
        return RTResult().success(Number.none)

    @set_args(["string", "value", "with", "c"], [None, None, None, Number(-1)])
    def execute_replace_fp(self, exec_ctx):
        string = exec_ctx.symbol_table.get("string")
        value = exec_ctx.symbol_table.get("value")
        with_val = exec_ctx.symbol_table.get("with")
        c = exec_ctx.symbol_table.get("c")
        if not isinstance(string, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'replace' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(value, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'replace' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(with_val, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'replace' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(with_val, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Fourth argument of 'replace' must be a string",
                    exec_ctx,
                )
            )
        val = string.value.replace(value.value, with_val.value, c)
        return RTResult().success(String(val))

    @set_args(["value"])
    def execute_len(self, exec_ctx):
        value_ = exec_ctx.symbol_table.get("value")
        if isinstance(value_, List | String | Bytes | HashMap):
            return RTResult().success(Number(len(value_.value)))
        else:
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'len' must be a list, string, hashmap or bytes",
                    exec_ctx,
                )
            )

    @set_args(["seconds"])
    def execute_sleep_fp(self, exec_ctx):
        seconds = exec_ctx.symbol_table.get("seconds")
        if not isinstance(seconds, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'sleep' must be a number",
                    exec_ctx,
                )
            )
        time.sleep(seconds.value)
        return RTResult().success(Number.none)

    @set_args(["value"], [0])
    def execute_exit_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        sys.exit(int(value.value))

    @set_args(
        ["l", "start", "end", "step"], [None, Number.none, Number.none, Number.none]
    )
    def execute_slice(self, exec_ctx):
        l = exec_ctx.symbol_table.get("l")
        start = exec_ctx.symbol_table.get("start")
        end = exec_ctx.symbol_table.get("end")
        step = exec_ctx.symbol_table.get("step")
        if not isinstance(l, String | List | HashMap):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'slice' must be a string, list, hashmap or bytes",
                    exec_ctx,
                )
            )
        if not isinstance(start, Number) and not isinstance(start, NoneObject):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'slice' must be a number or none",
                    exec_ctx,
                )
            )
        if not isinstance(end, Number) and not isinstance(end, NoneObject):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'slice' must be a number or none",
                    exec_ctx,
                )
            )
        if not isinstance(step, Number) and not isinstance(step, NoneObject):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Fourth argument of 'slice' must be a number or none",
                    exec_ctx,
                )
            )
        a = int(start.value) if not isinstance(start, NoneObject) else None
        b = int(end.value) if not isinstance(end, NoneObject) else None
        s = int(step.value) if not isinstance(step, NoneObject) else None
        if isinstance(l, String):
            sliced_l = l.value[a:b:s]
            return RTResult().success(String(sliced_l))
        elif isinstance(l, HashMap):
            sliced_l = dict(l.value.items()[a:b:s])
            return RTResult().success(HashMap(sliced_l))
        elif isinstance(l, Bytes):
            sliced_l = l.value[a:b:s]
            return RTResult().success(Bytes(sliced_l))
        sliced_l = l.value[a:b:s]
        return RTResult().success(List(sliced_l))

    @set_args(["file_path"])
    def execute_open_fp(self, exec_ctx):
        file_path = exec_ctx.symbol_table.get("file_path")
        try:
            file_name = os.path.splitext(file_path.value)[0]
            return RTResult().success(File(file_name, file_path.value))
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f'Failed to open file "{file_path.value}": ' + str(e),
                    exec_ctx,
                )
            )

    @set_args(["file", "mode"])
    def execute_read_fp(self, exec_ctx):
        file = exec_ctx.symbol_table.get("file")
        mode = exec_ctx.symbol_table.get("mode")
        if mode.value == "r":
            try:
                with open(file.path.__str__(), "r", encoding="utf-8") as f:
                    return RTResult().success(String(f.read()))
            except Exception as e:
                return RTResult().failure(
                    IError(
                        self.pos_start,
                        self.pos_end,
                        f'Failed to read file "{file.path}"\n' + str(e),
                        exec_ctx,
                    )
                )
        elif mode.value == "rb":
            try:
                with open(file.path.__str__(), "rb") as f:
                    return RTResult().success(Bytes(f.read()))
            except Exception as e:
                return RTResult().failure(
                    IError(
                        self.pos_start,
                        self.pos_end,
                        f'Failed to read file "{file.path}": ' + str(e),
                        exec_ctx,
                    )
                )

    @set_args(["file", "mode", "text"])
    def execute_write_fp(self, exec_ctx):
        file = exec_ctx.symbol_table.get("file")
        mode = exec_ctx.symbol_table.get("mode")
        text = exec_ctx.symbol_table.get("text")
        try:
            with open(
                file.path.__str__(),
                mode.__str__(),
                encoding="utf-8" if mode.value == "w" or mode.value == "a" else None,
            ) as f:
                f.write(text.value)
            return RTResult().success(Number.none)
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f'Failed to write to file "{file.path}": ' + str(e),
                    exec_ctx,
                )
            )

    @set_args(["file_path"])
    def execute_exists_fp(self, exec_ctx):
        file_path = exec_ctx.symbol_table.get("file_path")
        if isinstance(file_path, String):
            file_path = file_path.value
        elif isinstance(file_path, File):
            file_path = file_path.path
        else:
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'exists' must be a string",
                    exec_ctx,
                )
            )
        try:
            return RTResult().success(
                Number.true if os.path.exists(file_path) else Number.false
            )
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to check if file exists '{file_path}': " + str(e),
                    exec_ctx,
                )
            )

    @set_args([])
    def execute_time_fp(self, _):
        return RTResult().success(Number(time.time()))

    @set_args(["name"])
    def execute_get_env_fp(self, exec_ctx):
        name = exec_ctx.symbol_table.get("name")
        if not isinstance(name, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'get_env' must be a string",
                    exec_ctx,
                )
            )
        value = os.getenv(name.value)
        if value is None:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Environment variable '{name.value}' does not exist",
                    exec_ctx,
                )
            )
        return RTResult().success(String(value))

    @set_args(["name", "value"])
    def execute_set_env_fp(self, exec_ctx):
        name = exec_ctx.symbol_table.get("name")
        value = exec_ctx.symbol_table.get("value")
        if not isinstance(name, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'set_env' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(value, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'set_env' must be a string",
                    exec_ctx,
                )
            )
        try:
            os.environ[name.value] = value.value
            return RTResult().success(Number.none)
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to set environment variable '{name.value}': " + str(e),
                    exec_ctx,
                )
            )

    @set_args([])
    def execute_get_cdir_fp(self, exec_ctx):
        try:
            return RTResult().success(String(os.getcwd()))
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to get current directory: " + str(e),
                    exec_ctx,
                )
            )

    @set_args(["name"])
    def execute_set_cdir_fp(self, exec_ctx):
        name = exec_ctx.symbol_table.get("name")
        if not isinstance(name, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'set_cdir' must be a string",
                    exec_ctx,
                )
            )
        if not os.path.exists(name.value):
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Directory '{name.value}' does not exist",
                    exec_ctx,
                )
            )
        try:
            os.chdir(name.value)
            return RTResult().success(Number.none)
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to set current directory to '{name.value}': " + str(e),
                    exec_ctx,
                )
            )

    @set_args([])
    def execute_rand_fp(self, _):
        return RTResult().success(Number(random.random()))

    @set_args(["min", "max"])
    def execute_rand_int_fp(self, exec_ctx):
        min = exec_ctx.symbol_table.get("min")
        max = exec_ctx.symbol_table.get("max")
        if not isinstance(min, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'rand_int' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(max, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'rand_int' must be a number",
                    exec_ctx,
                )
            )
        return RTResult().success(
            Number(random.randint(int(min.value), int(max.value)))
        )

    @set_args(["min", "max"])
    def execute_rand_float_fp(self, exec_ctx):
        min = exec_ctx.symbol_table.get("min")
        max = exec_ctx.symbol_table.get("max")
        if not isinstance(min, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'rand_float' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(max, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'rand_float' must be a number",
                    exec_ctx,
                )
            )
        return RTResult().success(Number(random.randint(min.value, max.value)))

    @set_args(["arr"])
    def execute_rand_choice_fp(self, exec_ctx):
        arr = exec_ctx.symbol_table.get("arr")
        if not isinstance(arr, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'rand_choice' must be a list",
                    exec_ctx,
                )
            )
        if len(arr.value) == 0:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Array passed to 'rand_choice' is empty",
                    exec_ctx,
                )
            )
        return RTResult().success(arr.value[random.randrange(0, len(arr.value) - 1)])

    @set_args(["value"])
    def execute_to_str(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get("value"))))

    @set_args(["value", "supress_error"], [None, Number.false])
    def execute_to_int(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        supress_error = exec_ctx.symbol_table.get("supress_error")
        if not isinstance(supress_error, Bool):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'to_int' must be a boolean",
                    exec_ctx,
                )
            )
        if int(supress_error.value) == 1:
            supress_error_ = True
        elif int(supress_error.value) == 0:
            supress_error_ = False
        else:
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'to_int' must be a boolean",
                    exec_ctx,
                )
            )
        if isinstance(value, Number):
            return RTResult().success(Number(int(value.value)))
        elif isinstance(value, String):
            try:
                return RTResult().success(Number(int(value.value)))
            except ValueError:
                if supress_error_:
                    return RTResult().success(Number.none)
                else:
                    return RTResult().failure(
                        RTError(
                            self.pos_start,
                            self.pos_end,
                            f"Failed to convert '{value.value}' of type '{value.type()}' to integer",
                            exec_ctx,
                        )
                    )
        else:
            if supress_error_:
                return RTResult().success(Number.none)
            else:
                return RTResult().failure(
                    TError(
                        self.pos_start,
                        self.pos_end,
                        f"Failed to convert value of type '{value.type()}' to integer",
                        exec_ctx,
                    )
                )

    @set_args(["value", "supress_error"], [None, Number.false])
    def execute_to_float(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        supress_error = exec_ctx.symbol_table.get("supress_error")
        if not isinstance(supress_error, Bool):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'to_float' must be a boolean",
                    exec_ctx,
                )
            )
        if int(supress_error.value) == 1:
            supress_error_ = True
        elif int(supress_error.value) == 0:
            supress_error_ = False
        else:
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'to_float' must be a boolean",
                    exec_ctx,
                )
            )
        if isinstance(value, Number):
            return RTResult().success(Number(float(value.value)))
        elif isinstance(value, String):
            try:
                return RTResult().success(Number(float(value.value)))
            except ValueError:
                if supress_error_:
                    return RTResult().success(Number.none)
                else:
                    return RTResult().failure(
                        RTError(
                            self.pos_start,
                            self.pos_end,
                            f"Failed to convert '{value.value}' of type '{value.type()}' to float",
                            exec_ctx,
                        )
                    )
        else:
            if supress_error_:
                return RTResult().success(Number.none)
            else:
                return RTResult().failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        f"Failed to convert value of type '{value.type()}' to float",
                        exec_ctx,
                    )
                )

    @set_args(["sep", "value"])
    def execute_join_fp(self, exec_ctx):
        sep = exec_ctx.symbol_table.get("sep")
        iterables = exec_ctx.symbol_table.get("value")
        if not isinstance(sep, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'join' must be a string",
                    exec_ctx,
                )
            )
        if isinstance(iterables, List):
            if len(iterables.value) == 0:
                return RTResult().success(String(""))
            return RTResult().success(
                String(sep.value.join([str(element) for element in iterables.value]))
            )
        elif isinstance(iterables, String):
            if len(iterables) == 0:
                return RTResult().success(String(""))
            return RTResult().success(
                String(sep.value.join([str(element) for element in iterables.value]))
            )
        else:
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'join' must be a list or a string",
                    exec_ctx,
                )
            )

    @set_args(["command"])
    def execute_system_fp(self, exec_ctx):
        command = exec_ctx.symbol_table.get("command")
        if not isinstance(command, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'system' must be a string",
                    exec_ctx,
                )
            )
        try:
            os.system(command.value)
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to execute '{command.value}': " + str(e),
                    exec_ctx,
                )
            )
        return RTResult().success(Number.none)

    @set_args(["command"])
    def execute_osystem_fp(self, exec_ctx):
        cmd = exec_ctx.symbol_table.get("cmd")
        result = subprocess.run(
            cmd.value,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return RTResult().success(
            List(
                [
                    String(result.stdout),
                    String(result.stderr),
                    Number(result.returncode),
                ]
            )
        )

    @set_args(["message", "err_type"], [None, String("RT")])
    def execute_panic(self, exec_ctx):
        msg = exec_ctx.symbol_table.get("message")
        err_type = exec_ctx.symbol_table.get("err_type")
        if not isinstance(msg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'panic' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(err_type, String):
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'panic' must be a string ('RT': 'Runtime Error', 'M': 'Math Error', 'IO': 'IO Error' or 'T': 'Type Error')",
                    exec_ctx,
                )
            )
        err_type_value = err_type.value.upper().strip()
        if err_type_value == "RT":
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end, msg, exec_ctx)
            )
        elif err_type_value == "M":
            return RTResult().failure(
                MError(self.pos_start, self.pos_end, msg, exec_ctx)
            )
        elif err_type_value == "IO":
            return RTResult().failure(
                IError(self.pos_start, self.pos_end, msg, exec_ctx)
            )
        elif err_type_value == "T":
            return RTResult().failure(
                TError(self.pos_start, self.pos_end, msg, exec_ctx)
            )
        else:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'panic' must be a string ('RT': 'Runtime Error', 'M': 'Math Error', 'IO': 'IO Error' or 'T': 'Type Error')",
                    exec_ctx,
                )
            )

    @set_args(["string", "sep"], [None, String("")])
    def execute_split_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("string")
        sep = exec_ctx.symbol_table.get("sep")
        if not isinstance(value, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'split' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(sep, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'split' must be a string",
                    exec_ctx,
                )
            )
        if len(sep.value) == 0:
            return RTResult().success(
                List([String(string) for string in list(value.value)])
            )
        return RTResult().success(
            List([String(string) for string in value.value.split(sep.value)])
        )

    @set_args(["string", "sep"], [None, String(" ")])
    def execute_strip_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("string")
        sep = exec_ctx.symbol_table.get("sep")
        if not isinstance(value, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'strip' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(sep, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'strip' must be a string",
                    exec_ctx,
                )
            )
        return RTResult().success(String(value.value.strip(sep.value)))

    @set_args(["string"])
    def execute_to_upper_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("string")
        if not isinstance(value, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'to_upper' must be a string",
                    exec_ctx,
                )
            )
        return RTResult().success(String(value.value.upper()))

    @set_args(["string"])
    def execute_to_lower_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("string")
        if not isinstance(value, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'to_lower' must be a string",
                    exec_ctx,
                )
            )
        return RTResult().success(String(value.value.lower()))

    @set_args(["time"])
    def execute_ctime_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("time")
        if not isinstance(value, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'ctime' must be a number",
                    exec_ctx,
                )
            )
        return RTResult().success(String(time.ctime(int(value.value))))

    @set_args(["dir_path"], [String(".")])
    def execute_list_dir_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("dir_path")
        if not isinstance(value, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'list_dir' must be a string",
                    exec_ctx,
                )
            )
        if not os.path.isdir(value.value):
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Directory '{value.value}' does not exist",
                    exec_ctx,
                )
            )
        try:
            return RTResult().success(
                List([String(string) for string in os.listdir(value.value)])
            )
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to list directory: {e}",
                    exec_ctx,
                )
            )

    @set_args(["dir_path"])
    def execute_mkdir_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("dir_path")
        if not isinstance(value, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'make_dir' must be a string",
                    exec_ctx,
                )
            )
        if os.path.exists(value.value):
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Directory '{value.value}' already exists",
                    exec_ctx,
                )
            )
        os.mkdir(value.value)
        return RTResult().success(Number.none)

    @set_args(["file_path"])
    def execute_remove_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("file_path")
        if not isinstance(value, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'remove_file' must be a string",
                    exec_ctx,
                )
            )
        if not os.path.exists(value.value):
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"File '{value.value}' does not exist",
                    exec_ctx,
                )
            )
        try:
            os.remove(value.value)
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to remove file: " + str(e),
                    exec_ctx,
                )
            )
        return RTResult().success(Number.none)

    @set_args(["old_file_path", "new_file_path"])
    def execute_rename_fp(self, exec_ctx):
        value1 = exec_ctx.symbol_table.get("old_file_path")
        value2 = exec_ctx.symbol_table.get("new_file_path")
        if not isinstance(value1, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'rename' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(value2, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'rename' must be a string",
                    exec_ctx,
                )
            )
        if not os.path.exists(value1.value):
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"File or directory '{value1.value}' does not exist",
                    exec_ctx,
                )
            )
        try:
            os.rename(value1.value, value2.value)
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to rename file: {e}",
                    exec_ctx,
                )
            )
        return RTResult().success(Number.none)

    @set_args(["dir_path"])
    def execute_rmtree_fp(self, exec_ctx):
        value1 = exec_ctx.symbol_table.get("dir_path")
        if not isinstance(value1, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'remove_dir' must be a string",
                    exec_ctx,
                )
            )
        if not os.path.isdir(value1.value):
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"'{value1.value}' is not a directory",
                    exec_ctx,
                )
            )
        try:
            rmtree(value1.value)
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to remove directory: {e}",
                    exec_ctx,
                )
            )
        return RTResult().success(Number.none)

    @set_args(["src_path", "dst_path"])
    def execute_copy_fp(self, exec_ctx):
        value1 = exec_ctx.symbol_table.get("src_path")
        value2 = exec_ctx.symbol_table.get("dst_path")
        if not isinstance(value1, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'copy' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(value2, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'copy' must be a string",
                    exec_ctx,
                )
            )
        if not os.path.exists(value1.value):
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"'{value1.value}' does not exist",
                    exec_ctx,
                )
            )
        try:
            copy(value1.value, value2.value)
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to copy file: {e}",
                    exec_ctx,
                )
            )
        return RTResult().success(Number.none)

    @set_args(["text"])
    def execute_keyboard_write_fp(self, exec_ctx):
        text = exec_ctx.symbol_table.get("text")
        if not isinstance(text, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'write' must be a string",
                    exec_ctx,
                )
            )
        try:
            import keyboard  # type: ignore

            keyboard.write(text.value)
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "keyboard module not available",
                    exec_ctx,
                )
            )
        return RTResult().success(Number.none)

    @set_args(["key"])
    def execute_keyboard_press_fp(self, exec_ctx):
        key = exec_ctx.symbol_table.get("key")
        if not isinstance(key, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'press' must be a string",
                    exec_ctx,
                )
            )
        try:
            import keyboard  # type: ignore

            keyboard.press(key.value)
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "keyboard module not available",
                    exec_ctx,
                )
            )
        return RTResult().success(Number.none)

    @set_args(["key"])
    def execute_keyboard_release_fp(self, exec_ctx):
        key = exec_ctx.symbol_table.get("key")
        if not isinstance(key, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'release' must be a string",
                    exec_ctx,
                )
            )
        try:
            import keyboard  # type: ignore

            keyboard.release(key.value)
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "keyboard module not available",
                    exec_ctx,
                )
            )
        return RTResult().success(Number.none)

    @set_args(["key"])
    def execute_keyboard_wait_fp(self, exec_ctx):
        key = exec_ctx.symbol_table.get("key")
        if not isinstance(key, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'wait' must be a string",
                    exec_ctx,
                )
            )
        try:
            import keyboard  # type: ignore

            keyboard.wait(key.value)
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "keyboard module not available",
                    exec_ctx,
                )
            )
        return RTResult().success(Number.none)

    @set_args(["key"])
    def execute_keyboard_is_pressed_fp(self, exec_ctx):
        key = exec_ctx.symbol_table.get("key")
        if not isinstance(key, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'is_pressed' must be a string",
                    exec_ctx,
                )
            )
        try:
            import keyboard  # type: ignore

            is_pressed = keyboard.is_pressed(key.value)
            return RTResult().success(Number.true if is_pressed else Number.false)
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "keyboard module not available",
                    exec_ctx,
                )
            )

    @set_args(["func", "args", "kwargs"], [None, List([]), HashMap({})])
    def execute_thread_start_fp(self, exec_ctx):
        func = exec_ctx.symbol_table.get("func")
        args = exec_ctx.symbol_table.get("args")
        kwargs = exec_ctx.symbol_table.get("kwargs")

        if not isinstance(func, BaseFunction):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'start' must be a function",
                    exec_ctx,
                )
            )
        if not isinstance(args, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'start' must be a list",
                    exec_ctx,
                )
            )
        if not isinstance(kwargs, HashMap):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'start' must be a hashmap",
                    exec_ctx,
                )
            )

        positional_args = args.value
        keyword_args = {
            k.value: v for k, v in kwargs.value.items() if hasattr(k, "value")
        }

        def thread_wrapper():
            try:
                result = func.execute(positional_args, keyword_args)
                if result and result.error:
                    sys.stderr.write(str(result.error) + "\n")
                    sys.stderr.flush()

            except Exception:
                error_header = (
                    f"\n--- Python Exception in Thread (Function: {func.name}) ---\n"
                )
                sys.stderr.write(error_header)
                import traceback

                sys.stderr.write(traceback.format_exc() + "\n")
                sys.stderr.flush()

        try:
            thread = Thread(target=thread_wrapper, daemon=True)
            thread.start()
            return RTResult().success(ThreadWrapper(thread))
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to start thread: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["seconds"])
    def execute_thread_sleep_fp(self, exec_ctx):
        seconds = exec_ctx.symbol_table.get("seconds")
        if not isinstance(seconds, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'sleep' must be a number",
                    exec_ctx,
                )
            )
        try:
            import time

            time.sleep(seconds.value)
            return RTResult().success(Number.none)
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to sleep thread: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["thread", "timeout"], [None, Number(15)])
    def execute_thread_join_fp(self, exec_ctx):
        thread = exec_ctx.symbol_table.get("thread")
        timeout = exec_ctx.symbol_table.get("timeout")
        if not isinstance(thread, ThreadWrapper):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'join' must be a thread",
                    exec_ctx,
                )
            )
        if not isinstance(timeout, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'join' must be a number",
                    exec_ctx,
                )
            )
        try:
            thread.join(timeout.value)
            return RTResult().success(Number.none)
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to join thread: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["thread"])
    def execute_thread_is_alive_fp(self, exec_ctx):
        thread = exec_ctx.symbol_table.get("thread")
        if not isinstance(thread, ThreadWrapper):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'is_alive' must be a thread",
                    exec_ctx,
                )
            )
        return RTResult().success(Number.true if thread.is_alive() else Number.false)

    @set_args(["thread"])
    def execute_thread_cancel_fp(self, exec_ctx):
        thread = exec_ctx.symbol_table.get("thread")
        if not isinstance(thread, ThreadWrapper):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'cancel' must be a thread",
                    exec_ctx,
                )
            )
        try:
            thread.cancel()
            return RTResult().success(Number.none)
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to cancel thread: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["thread"])
    def execute_is_thread(self, exec_ctx):
        thread = exec_ctx.symbol_table.get("thread")
        return RTResult().success(
            Number.true if isinstance(thread, ThreadWrapper) else Number.false
        )

    @set_args(["value"])
    def execute_ord_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        if not isinstance(value, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'ord' must be a string",
                    exec_ctx,
                )
            )
        if len(value.value) != 1:
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "String passed to 'ord' must be a single character",
                    exec_ctx,
                )
            )
        return RTResult().success(Number(ord(value.value)))

    @set_args(["value"])
    def execute_chr_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        if not isinstance(value, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'char' must be a number",
                    exec_ctx,
                )
            )
        try:
            return RTResult().success(String(chr(int(value.value))))
        except ValueError:
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Value passed to 'char' is out of range",
                    exec_ctx,
                )
            )

    @set_args([])
    def execute_get_ip_fp(self, exec_ctx):
        try:
            with urllib.request.urlopen("https://api.ipify.org") as res_:
                return RTResult().success(String(res_.read().decode()))
        except:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Failed to retrieve IP address",
                    exec_ctx,
                )
            )

    @set_args([])
    def execute_get_mac_fp(self, exec_ctx):
        try:
            mac = uuid.getnode()
            mac_addr = ":".join(
                ["{:02x}".format((mac >> ele) & 0xFF) for ele in range(40, -1, -8)]
            )
            return RTResult().success(String(mac_addr))
        except:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Failed to retrieve MAC address",
                    exec_ctx,
                )
            )

    @set_args(["host"])
    def execute_ping_fp(self, exec_ctx):
        host = exec_ctx.symbol_table.get("host")
        if not isinstance(host, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'ping' must be a string",
                    exec_ctx,
                )
            )

        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", host.value]

        try:
            subprocess.check_call(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return RTResult().success(Number.true)
        except subprocess.CalledProcessError:
            return RTResult().success(Number.false)
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error while pinging host: {e}",
                    exec_ctx,
                )
            )

    @set_args(["url", "timeout"], [None, Number(15)])
    def execute_downl_fp(self, exec_ctx):
        def sanitize_filename(filename):
            filename = unquote(filename)
            filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
            return filename or "downl_" + hex(time.time_ns())[2:]

        url: String = exec_ctx.symbol_table.get("url")
        timeout: Number = exec_ctx.symbol_table.get("timeout")
        if not isinstance(url, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'download' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(timeout, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'download' must be a number",
                    exec_ctx,
                )
            )
        try:
            req = urllib.request.Request(
                url.value,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            )
            with urllib.request.urlopen(req, timeout=timeout.value) as response:
                cd = response.headers.get("Content-Disposition")
                if cd:
                    fname = re.findall('filename="(.+)"', cd)
                    name = (
                        sanitize_filename(fname[0])
                        if fname
                        else url.value.split("/")[-1]
                    )
                else:
                    name = url.value.split("/")[-1]
                name = sanitize_filename(name)
                if not name:
                    name = "download_" + hex(time.time_ns())[2:]
                with open(name, "wb") as out_file:
                    out_file.write(response.read())
            return RTResult().success(String(os.path.abspath(name)))
        except urllib.error.HTTPError as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"HTTP Error {e.code}: Failed to download {url.value}",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to download {url.value}: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args([])
    def execute_get_local_ip_fp(self, exec_ctx):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return RTResult().success(String(ip))
        except:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Failed to retrieve local IP address",
                    exec_ctx,
                )
            )

    @set_args([])
    def execute_get_hostname_fp(self, exec_ctx):
        try:
            return RTResult().success(String(socket.gethostname()))
        except:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Failed to retrieve hostname",
                    exec_ctx,
                )
            )

    @set_args(["text"])
    def execute_md5_fp(self, exec_ctx):
        text = exec_ctx.symbol_table.get("text")
        if not isinstance(text, Bytes):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'md5' must be a bytes",
                    exec_ctx,
                )
            )
        return RTResult().success(Bytes(hashlib.md5(text.value).hexdigest().encode()))

    @set_args(["text"])
    def execute_sha1_fp(self, exec_ctx):
        text = exec_ctx.symbol_table.get("text")
        if not isinstance(text, Bytes):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'sha1' must be a bytes",
                    exec_ctx,
                )
            )
        return RTResult().success(Bytes(hashlib.sha1(text.value).hexdigest().encode()))

    @set_args(["text"])
    def execute_sha256_fp(self, exec_ctx):
        text = exec_ctx.symbol_table.get("text")
        if not isinstance(text, Bytes):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'sha256' must be a bytes",
                    exec_ctx,
                )
            )
        return RTResult().success(
            Bytes(hashlib.sha256(text.value).hexdigest().encode())
        )

    @set_args(["text"])
    def execute_sha512_fp(self, exec_ctx):
        text = exec_ctx.symbol_table.get("text")
        if not isinstance(text, Bytes):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'sha512' must be a bytes",
                    exec_ctx,
                )
            )
        return RTResult().success(
            Bytes(hashlib.sha512(text.value).hexdigest().encode())
        )

    @set_args(["text"])
    def execute_crc32_fp(self, exec_ctx):
        text = exec_ctx.symbol_table.get("text")
        if not isinstance(text, Bytes):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'crc32' must be a bytes",
                    exec_ctx,
                )
            )
        return RTResult().success(
            Bytes(format(zlib.crc32(text.value) & 0xFFFFFFFF, "08x").encode())
        )

    @set_args(["text", "substring"])
    def execute_find_fp(self, exec_ctx):
        text = exec_ctx.symbol_table.get("text")
        substring = exec_ctx.symbol_table.get("substring")
        if not isinstance(text, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'find' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(substring, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'find' must be a string",
                    exec_ctx,
                )
            )
        index = text.value.find(substring.value)
        if index == -1:
            return RTResult().success(Number.none)
        return RTResult().success(Number(index))

    def _handle_panic_result(self, res, exec_ctx):
        if res.error:
            err = res.error
            if isinstance(err, RTError):
                err_str = str(err)
                err_line = err_str.strip().split("\n")[-1]
                err_name, err_msg = err_line.split(":", 1)
                err_name, err_msg = err_name.strip(), err_msg.strip()

                err_name = re.sub(
                    r"^(?:\x1b\[[0-9;]*m)+|(?:\x1b\[[0-9;]*m)+$", "", err_name
                )
                err_msg = re.sub(
                    r"^(?:\x1b\[[0-9;]*m)+|(?:\x1b\[[0-9;]*m)+$", "", err_msg
                )

                if "Runtime" in err_name:
                    err_name_short = "RT"
                elif "Math" in err_name:
                    err_name_short = "M"
                elif "IO" in err_name:
                    err_name_short = "IO"
                elif "Type" in err_name:
                    err_name_short = "T"
                else:
                    err_name_short = "UNKNOWN"

                return RTResult().success(
                    List([Number.none, String(err_msg), String(err_name_short)])
                )
            else:
                return RTResult().failure(err)
        else:
            return RTResult().success(List([res.value, Number.none, Number.none]))

    @set_args(["func", "args", "kwargs"], [None, List([]), HashMap({})])
    def execute_is_panic(self, exec_ctx):
        func = exec_ctx.symbol_table.get("func")
        args = exec_ctx.symbol_table.get("args")
        kwargs = exec_ctx.symbol_table.get("kwargs")

        if not isinstance(func, BaseFunction):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'is_panic' must be a function",
                    exec_ctx,
                )
            )
        if not isinstance(args, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'is_panic' must be a list",
                    exec_ctx,
                )
            )
        if not isinstance(kwargs, HashMap):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'is_panic' must be a hashmap",
                    exec_ctx,
                )
            )

        try:
            positional_args = args.value
            keyword_args = kwargs.value

            res = func.execute(positional_args, keyword_args)

            return self._handle_panic_result(res, exec_ctx)

        except Exception as err:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Unexpected Python error in 'is_panic': {err}",
                    exec_ctx,
                )
            )

    @set_args(["path"])
    def execute_is_file_fp(self, exec_ctx):
        path = exec_ctx.symbol_table.get("path")
        if not isinstance(path, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'is_file' must be a string",
                    exec_ctx,
                )
            )
        return RTResult().success(
            Number.true if os.path.isfile(path.value) else Number.false
        )

    @set_args(["a"])
    def execute_sqrt_fp(self, exec_ctx):
        a = exec_ctx.symbol_table.get("a")
        try:
            return RTResult().success(Number(math.sqrt(a.value)))
        except ValueError:
            RTResult().failure(
                MError(
                    self.pos_start,
                    self.pos_end,
                    "Math domain error",
                    self.context,
                )
            )

    @set_args(["a"])
    def execute_abs_fp(self, exec_ctx):
        a = exec_ctx.symbol_table.get("a")
        return RTResult().success(Number(abs(a.value)))

    @set_args(["x"])
    def execute_sin_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        return RTResult().success(Number(math.sin(x.value)))

    @set_args(["x"])
    def execute_cos_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        return RTResult().success(Number(math.cos(x.value)))

    @set_args(["x"])
    def execute_tan_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        return RTResult().success(Number(math.tan(x.value)))

    @set_args(["n"])
    def execute_fact_fp(self, exec_ctx):
        n = exec_ctx.symbol_table.get("n")
        return RTResult().success(Number(math.factorial(n.value)))

    @set_args(["a", "b"])
    def execute_gcd_fp(self, exec_ctx):
        a = exec_ctx.symbol_table.get("a")
        b = exec_ctx.symbol_table.get("b")
        return RTResult().success(Number(math.gcd(a.value, b.value)))

    @set_args(["a", "b"])
    def execute_lcm_fp(self, exec_ctx):
        a = exec_ctx.symbol_table.get("a")
        b = exec_ctx.symbol_table.get("b")
        return RTResult().success(Number(math.lcm(a.value, b.value)))

    @set_args(["n"])
    def execute_fib_fp(self, exec_ctx):
        n = exec_ctx.symbol_table.get("n")
        if n.value == 0:
            return RTResult().success(Number(0))
        a, b = 0, 1
        for _ in range(n.value):
            a, b = b, a + b
        return RTResult().success(Number(a))

    @set_args(["n"])
    def execute_is_prime_fp(self, exec_ctx):
        n = exec_ctx.symbol_table.get("n").value
        if n < 2:
            return RTResult().success(Number.false)
        if n == 2 or n == 3:
            return RTResult().success(Number.true)
        if n % 2 == 0 or n % 3 == 0:
            return RTResult().success(Number.false)
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return RTResult().success(Number.false)
            i += 6
        return RTResult().success(Number.true)

    @set_args(["d"])
    def execute_deg2rad_fp(self, exec_ctx):
        d = exec_ctx.symbol_table.get("d")
        return RTResult().success(Number(math.radians(d.value)))

    @set_args(["r"])
    def execute_rad2deg_fp(self, exec_ctx):
        r = exec_ctx.symbol_table.get("r")
        return RTResult().success(Number(math.degrees(r.value)))

    @set_args(["x"])
    def execute_exp_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        return RTResult().success(Number(math.exp(x.value)))

    @set_args(["x"])
    def execute_log_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        return RTResult().success(Number(math.log(x.value)))

    @set_args(["x"])
    def execute_sinh_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        return RTResult().success(Number(math.sinh(x.value)))

    @set_args(["x"])
    def execute_cosh_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        return RTResult().success(Number(math.cosh(x.value)))

    @set_args(["x"])
    def execute_tanh_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        return RTResult().success(Number(math.tanh(x.value)))

    @set_args(["x"])
    def execute_round_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        return RTResult().success(Number(round(x.value)))

    def convert_zer_to_py(self, obj):
        if isinstance(obj, Number):
            return obj.value
        elif isinstance(obj, String):
            return obj.value
        elif isinstance(obj, NoneObject):
            return None
        elif isinstance(obj, List):
            return [self.convert_zer_to_py(e) for e in obj.value]
        elif isinstance(obj, HashMap):
            result = {}
            for k, v in obj.value.items():
                key = self.convert_zer_to_py(k)
                val = self.convert_zer_to_py(v)
                result[key] = val
            return result
        elif isinstance(obj, PyObject):
            return obj.get_obj()
        elif isinstance(obj, Bytes):
            return obj.value
        else:
            return str(obj)

    def validate_pyexec_result(self, obj):
        allowed = (bool, int, float, str)
        if obj is None:
            return Number.none
        elif isinstance(obj, allowed):
            if isinstance(obj, bool):
                if obj:
                    return Number.true
                else:
                    return Number.false
            elif isinstance(obj, int):
                return Number(obj)
            elif isinstance(obj, float):
                return Number(obj)
            elif isinstance(obj, bytes):
                return Bytes(obj)
            else:
                return String(obj)
        elif isinstance(obj, list):
            items = []
            for item in obj:
                if not isinstance(
                    item, (bool, int, float, str, list, dict, tuple, type(None), bytes)
                ):
                    items.append(String(str(item)))
                else:
                    items.append(self.validate_pyexec_result(item))
            return List(items)
        elif isinstance(obj, dict):
            new_dict = {}
            for k, v in obj.items():
                if not isinstance(k, (str, int, float, bool)):
                    key = String(str(k))
                    value = String(str(v))
                else:
                    key = self.validate_pyexec_result(k)
                    value = self.validate_pyexec_result(v)

                new_dict[key] = value
            return HashMap(new_dict)
        elif isinstance(obj, tuple):
            items = []
            for item in obj:
                if not isinstance(
                    item, (bool, int, float, str, list, dict, tuple, type(None))
                ):
                    items.append(self.validate_pyexec_result(String(str(obj))))
                else:
                    items.append(self.validate_pyexec_result(item))
            return List(items)
        else:
            return PyObject(obj)

    @set_args(["code", "env"], [None, HashMap({})])
    def execute_pyexec(self, exec_ctx):
        code = exec_ctx.symbol_table.get("code")
        args = exec_ctx.symbol_table.get("env")
        if not isinstance(code, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'pyexec' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(args, HashMap):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'pyexec' must be a hashmap",
                    exec_ctx,
                )
            )
        try:
            local_env = self.convert_zer_to_py(args)
            exec(code.value, {}, local_env)
            fr = self.validate_pyexec_result(local_env)
            return RTResult().success(fr)
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error executing code: {e}",
                    exec_ctx,
                )
            )

    @set_args(["path"])
    def execute_abs_path_fp(self, exec_ctx):
        path = exec_ctx.symbol_table.get("path")
        if not isinstance(path, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'abs_path' must be a string",
                    exec_ctx,
                )
            )
        try:
            return RTResult().success(String(os.path.abspath(path.value)))
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to get absolute path for '{path.value}': {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path"])
    def execute_dir_name_fp(self, exec_ctx):
        path = exec_ctx.symbol_table.get("path")
        if not isinstance(path, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'dir_name' must be a string",
                    exec_ctx,
                )
            )
        try:
            return RTResult().success(String(os.path.dirname(path.value)))
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to get directory name for '{path.value}': {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path"])
    def execute_base_name_fp(self, exec_ctx):
        path = exec_ctx.symbol_table.get("path")
        if not isinstance(path, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'base_name' must be a string",
                    exec_ctx,
                )
            )
        try:
            return RTResult().success(String(os.path.basename(path.value)))
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to get base name for '{path.value}': {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["src", "dst"])
    def execute_symlink_fp(self, exec_ctx):
        src = exec_ctx.symbol_table.get("src")
        dst = exec_ctx.symbol_table.get("dst")
        if not isinstance(src, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'symlink' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(dst, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'symlink' must be a string",
                    exec_ctx,
                )
            )
        try:
            if hasattr(os, "symlink"):
                os.symlink(src.value, dst.value)
                return RTResult().success(Number.none)
            else:
                return RTResult().failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        "Symbolic links are not supported on this system or require special privileges",
                        exec_ctx,
                    )
                )
        except OSError as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"OS error creating symlink '{src.value}' -> '{dst.value}': {str(e)}",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error creating symlink: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path"])
    def execute_readlink_fp(self, exec_ctx):
        path_arg = exec_ctx.symbol_table.get("path")
        if not isinstance(path_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'readlink' must be a string",
                    exec_ctx,
                )
            )
        try:
            if hasattr(os, "readlink"):
                target_path = os.readlink(path_arg.value)
                return RTResult().success(String(target_path))
            else:
                return RTResult().failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        "Reading symbolic links is not supported on this system",
                        exec_ctx,
                    )
                )
        except OSError as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"OS error reading link '{path_arg.value}': {str(e)}",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error reading link: {str(e)}",
                    exec_ctx,
                )
            )

    def _format_stat_result_to_list(self, stat_res, context):
        return List(
            [
                Number(stat_res.st_mode),
                Number(stat_res.st_ino),
                Number(stat_res.st_dev),
                Number(stat_res.st_nlink),
                Number(stat_res.st_uid),
                Number(stat_res.st_gid),
                Number(stat_res.st_size),
                Number(stat_res.st_atime),
                Number(stat_res.st_mtime),
                Number(stat_res.st_ctime),
            ]
        )

    @set_args(["path"])
    def execute_stat_fp(self, exec_ctx):
        path_arg = exec_ctx.symbol_table.get("path")
        if not isinstance(path_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'stat' must be a string",
                    exec_ctx,
                )
            )
        try:
            stat_res_obj = os.stat(path_arg.value)
            return RTResult().success(
                self._format_stat_result_to_list(stat_res_obj, exec_ctx)
            )
        except OSError as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"OS error getting stat for '{path_arg.value}': {str(e)}",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error getting stat: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path"])
    def execute_lstat_fp(self, exec_ctx):
        path_arg = exec_ctx.symbol_table.get("path")
        if not isinstance(path_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'lstat' must be a string",
                    exec_ctx,
                )
            )
        try:
            stat_res_obj = None
            if hasattr(os, "lstat"):
                stat_res_obj = os.lstat(path_arg.value)
            else:
                stat_res_obj = os.stat(path_arg.value)
            return RTResult().success(
                self._format_stat_result_to_list(stat_res_obj, exec_ctx)
            )
        except OSError as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"OS error getting lstat for '{path_arg.value}': {str(e)}",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error getting lstat: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["top"])
    def execute_walk_fp(self, exec_ctx):
        top_path = exec_ctx.symbol_table.get("top")
        if not isinstance(top_path, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'walk' must be a string",
                    exec_ctx,
                )
            )
        try:
            walk_results_list_of_lists = []
            for root, dirs, files in os.walk(top_path.value):
                fun_root = String(root)
                fun_dirs = List([String(d) for d in dirs])
                fun_files = List([String(f) for f in files])
                walk_results_list_of_lists.append(List([fun_root, fun_dirs, fun_files]))
            return RTResult().success(List(walk_results_list_of_lists))
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error during directory walk starting at '{top_path.value}': {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path", "mode"])
    def execute_chmod_fp(self, exec_ctx):
        path_arg = exec_ctx.symbol_table.get("path")
        mode_arg = exec_ctx.symbol_table.get("mode")

        if not isinstance(path_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'chmod' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(mode_arg, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'chmod' must be a number",
                    exec_ctx,
                )
            )
        try:
            os.chmod(path_arg.value, int(mode_arg.value))
            return RTResult().success(Number.none)
        except OSError as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"OS error changing mode for '{path_arg.value}': {str(e)}",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error changing mode: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path", "uid", "gid"])
    def execute_chown_fp(self, exec_ctx):
        path_arg = exec_ctx.symbol_table.get("path")
        uid_arg = exec_ctx.symbol_table.get("uid")
        gid_arg = exec_ctx.symbol_table.get("gid")
        if not isinstance(path_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'chown' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(uid_arg, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'chown' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(gid_arg, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'chown' must be a number",
                    exec_ctx,
                )
            )
        try:
            if hasattr(os, "chown"):
                os.chown(path_arg.value, int(uid_arg.value), int(gid_arg.value))
                return RTResult().success(Number.none)
            else:
                return RTResult().failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        "Changing file ownership (chown) is not supported on this system",
                        exec_ctx,
                    )
                )
        except OSError as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"OS error changing ownership for '{path_arg.value}': {str(e)}",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error changing ownership: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path", "times"])
    def execute_utime_fp(self, exec_ctx):
        path_arg = exec_ctx.symbol_table.get("path")
        times_arg = exec_ctx.symbol_table.get("times")
        if not isinstance(path_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'utime' must be a string",
                    exec_ctx,
                )
            )
        actual_times_tuple = None
        if isinstance(times_arg, List):
            if (
                len(times_arg.value) == 2
                and isinstance(times_arg.value[0], Number)
                and isinstance(times_arg.value[1], Number)
            ):
                actual_times_tuple = (
                    times_arg.value[0].value,
                    times_arg.value[1].value,
                )
            else:
                return RTResult().failure(
                    TError(
                        self.pos_start,
                        self.pos_end,
                        "Second argument of 'utime', if a list, must contain two numbers (access_time, modification_time)",
                        exec_ctx,
                    )
                )
        elif isinstance(times_arg, NoneObject):
            actual_times_tuple = None
        else:
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'utime' must be a list of two numbers or none",
                    exec_ctx,
                )
            )
        try:
            os.utime(path_arg.value, actual_times_tuple)
            return RTResult().success(Number.none)
        except OSError as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"OS error setting times for '{path_arg.value}': {str(e)}",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error setting times: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["src", "dst"])
    def execute_link_fp(self, exec_ctx):
        src = exec_ctx.symbol_table.get("src")
        dst = exec_ctx.symbol_table.get("dst")
        if not isinstance(src, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'link' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(dst, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'link' must be a string",
                    exec_ctx,
                )
            )
        try:
            if hasattr(os, "link"):
                os.link(src.value, dst.value)
                return RTResult().success(Number.none)
            else:
                return RTResult().failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        "Creating hard links is not supported on this system or requires special privileges",
                        exec_ctx,
                    )
                )
        except OSError as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"OS error creating hard link '{src.value}' -> '{dst.value}': {str(e)}",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error creating hard link: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path"])
    def execute_unlink_fp(self, exec_ctx):
        path_arg = exec_ctx.symbol_table.get("path")
        if not isinstance(path_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'unlink' must be a string",
                    exec_ctx,
                )
            )
        if os.path.isdir(path_arg.value):
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Can't unlink '{path_arg.value}': It is a directory",
                    exec_ctx,
                )
            )
        if not os.path.exists(path_arg.value) and not os.path.islink(path_arg.value):
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"File or link '{path_arg.value}' does not exist",
                    exec_ctx,
                )
            )
        try:
            os.unlink(path_arg.value)
            return RTResult().success(Number.none)
        except OSError as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to remove file: {str(e)}",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error unlinking file/link: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path", "mode"])
    def execute_access_fp(self, exec_ctx):
        path_arg = exec_ctx.symbol_table.get("path")
        mode_arg = exec_ctx.symbol_table.get("mode")
        if not isinstance(path_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'access' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(mode_arg, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'access' must be a number",
                    exec_ctx,
                )
            )
        try:
            has_access = os.access(path_arg.value, int(mode_arg.value))
            return RTResult().success(Number.true if has_access else Number.false)
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error checking access for '{path_arg.value}': {str(e)}",
                    exec_ctx,
                )
            )

    @set_args([], vargs_name="args")
    def execute_path_join_fp(self, exec_ctx):
        args_list_obj = exec_ctx.symbol_table.get("args")
        if not isinstance(args_list_obj, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'path_join' must be a list of path components",
                    exec_ctx,
                )
            )
        path_components_str = []
        for i, item in enumerate(args_list_obj.value):
            if not isinstance(item, String):
                return RTResult().failure(
                    TError(
                        self.pos_start,
                        self.pos_end,
                        f"All path components for 'path_join' must be strings (component at index {i} is not)",
                        exec_ctx,
                    )
                )
            path_components_str.append(item.value)
        if not path_components_str:
            return RTResult().success(String(""))
        try:
            joined_path = os.path.join(*path_components_str)
            return RTResult().success(String(joined_path))
        except TypeError as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error joining path components: {str(e)}",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Unexpected error joining path: {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path"])
    def execute_is_dir_fp(self, exec_ctx):
        path_arg = exec_ctx.symbol_table.get("path")
        if not isinstance(path_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'is_dir' must be a string",
                    exec_ctx,
                )
            )
        try:
            is_dir = os.path.isdir(path_arg.value)
            return RTResult().success(Number.true if is_dir else Number.false)
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to check if path is directory '{path_arg.value}': {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path"])
    def execute_is_link_fp(self, exec_ctx):
        path_arg = exec_ctx.symbol_table.get("path")
        if not isinstance(path_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'is_link' must be a string",
                    exec_ctx,
                )
            )
        try:
            is_link = os.path.islink(path_arg.value)
            return RTResult().success(Number.true if is_link else Number.false)
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to check if path is symlink '{path_arg.value}': {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(["path"])
    def execute_is_mount_fp(self, exec_ctx):
        path_arg = exec_ctx.symbol_table.get("path")
        if not isinstance(path_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'is_mount' must be a string",
                    exec_ctx,
                )
            )
        try:
            is_mount = os.path.ismount(path_arg.value)
            return RTResult().success(Number.true if is_mount else Number.false)
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to check if path is mount point '{path_arg.value}': {str(e)}",
                    exec_ctx,
                )
            )

    @set_args(
        ["url", "method", "headers", "data", "timeout"],
        [None, None, None, None, Number(15)],
    )
    def execute_request_fp(self, exec_ctx):
        url_arg = exec_ctx.symbol_table.get("url")
        method_arg = exec_ctx.symbol_table.get("method")
        headers_arg = exec_ctx.symbol_table.get("headers")
        data_arg = exec_ctx.symbol_table.get("data")
        timeout_arg = exec_ctx.symbol_table.get("timeout")
        if not isinstance(url_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'request' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(method_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'request' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(headers_arg, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'request' must be a list",
                    exec_ctx,
                )
            )
        if not isinstance(data_arg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Fourth argument of 'request' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(timeout_arg, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Fifth argument of 'request' must be a number",
                    exec_ctx,
                )
            )
        try:
            import requests  # type: ignore

            response = requests.request(
                method_arg.value,
                url_arg.value,
                headers=self.convert_zer_to_py(headers_arg),
                data=self.convert_zer_to_py(data_arg),
                timeout=timeout_arg.value,
            )
            return RTResult().success(self.validate_pyexec_result(response.json()))
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "requests module not available",
                    exec_ctx,
                )
            )
        except requests.exceptions.RequestException as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Can not make request: {e}",
                    exec_ctx,
                )
            )

    @set_args(["hm"])
    def execute_keys(self, exec_ctx):
        hm = exec_ctx.symbol_table.get("hm")
        if not isinstance(hm, HashMap):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'keys' must be a hashmap",
                    exec_ctx,
                )
            )
        return RTResult().success(List([String(k) for k in hm.value.keys()]))

    @set_args(["hm"])
    def execute_values(self, exec_ctx):
        hm = exec_ctx.symbol_table.get("hm")
        if not isinstance(hm, HashMap):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'values' must be a hashmap",
                    exec_ctx,
                )
            )
        return RTResult().success(List(list(hm.value.values())))

    @set_args(["hm"])
    def execute_items(self, exec_ctx):
        hm = exec_ctx.symbol_table.get("hm")
        if not isinstance(hm, HashMap):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'items' must be a hashmap",
                    exec_ctx,
                )
            )
        return RTResult().success(
            List([List([String(k), v]) for k, v in hm.value.items()])
        )

    @set_args(["hm", "key"])
    def execute_has(self, exec_ctx):
        hm = exec_ctx.symbol_table.get("hm")
        key = exec_ctx.symbol_table.get("key")
        if not isinstance(hm, HashMap):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'has' must be a hashmap",
                    exec_ctx,
                )
            )
        found = any(
            k.value == key.value for k in hm.value.keys() if hasattr(k, "value")
        )
        return RTResult().success(Number.true if found else Number.false)

    @set_args(["hm", "key", "default"], [None, None, Number.none])
    def execute_get(self, exec_ctx):
        hm = exec_ctx.symbol_table.get("hm")
        key = exec_ctx.symbol_table.get("key")
        default = exec_ctx.symbol_table.get("default")
        if not isinstance(hm, (HashMap, List)):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'get' must be a hashmap or list",
                    exec_ctx,
                )
            )
        if isinstance(hm, HashMap):
            if not isinstance(key, String):
                return RTResult().failure(
                    TError(
                        self.pos_start,
                        self.pos_end,
                        "Second argument of 'get' must be a string when first argument is a hashmap",
                        exec_ctx,
                    )
                )
            try:
                return RTResult().success(hm.value[key.value])
            except:
                pass
        else:
            if not isinstance(key, Number):
                return RTResult().failure(
                    TError(
                        self.pos_start,
                        self.pos_end,
                        "Second argument of 'get' must be a number when first argument is a list",
                        exec_ctx,
                    )
                )
            if 0 <= key.value < len(hm.value):
                return RTResult().success(hm.value[int(key.value)])
        return RTResult().success(default)

    @set_args(["hm", "key"])
    def execute_del_key(self, exec_ctx):
        hm = exec_ctx.symbol_table.get("hm")
        key = exec_ctx.symbol_table.get("key")
        if not isinstance(hm, HashMap):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'del_key' must be a hashmap",
                    exec_ctx,
                )
            )
        key_to_del = None
        for k in hm.value.keys():
            if hasattr(k, "value") and k.value == key.value:
                key_to_del = k
                break
        if key_to_del is not None:
            del hm.value[key_to_del]
            return RTResult().success(hm)
        return RTResult().success(Number.none)

    @set_args(["space", "member", "default"], [None, None, Number.none])
    def execute_get_member(self, exec_ctx):
        hm = exec_ctx.symbol_table.get("space")
        key = exec_ctx.symbol_table.get("member")
        default = exec_ctx.symbol_table.get("default")
        if not isinstance(hm, NameSpace):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'get_member' must be a namespace",
                    exec_ctx,
                )
            )
        if not isinstance(key, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'get_member' must be a string",
                    exec_ctx,
                )
            )

        member_name_str = key.value
        member_value = hm.get(member_name_str)

        if member_value is None:
            return RTResult().success(default)

        return RTResult().success(member_value)

    @set_args(["x", "y"])
    def execute_mouse_move_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        y = exec_ctx.symbol_table.get("y")
        if not isinstance(x, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'move' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(y, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'move' must be a number",
                    exec_ctx,
                )
            )
        try:
            import pyautogui  # type: ignore

            pyautogui.moveTo(int(x.value), int(y.value))
            return RTResult().success(Number.none)
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "pyautogui module not available",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args([])
    def execute_mouse_click_fp(self, exec_ctx):
        try:
            import pyautogui  # type: ignore

            pyautogui.click()
            return RTResult().success(Number.none)
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "pyautogui module not available",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args([])
    def execute_mouse_right_click_fp(self, exec_ctx):
        try:
            import pyautogui  # type: ignore

            pyautogui.rightClick()
            return RTResult().success(Number.none)
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "pyautogui module not available",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(["amount"])
    def execute_mouse_scroll_fp(self, exec_ctx):
        amount = exec_ctx.symbol_table.get("amount")
        if not isinstance(amount, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'scroll' must be a number",
                    exec_ctx,
                )
            )
        try:
            import pyautogui  # type: ignore

            pyautogui.scroll(int(amount.value))
            return RTResult().success(Number.none)
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "pyautogui module not available",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args([])
    def execute_mouse_position_fp(self, exec_ctx):
        try:
            import pyautogui  # type: ignore

            x, y = pyautogui.position()
            return RTResult().success(List([Number(x), Number(y)]))
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "pyautogui module not available",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(["path"])
    def execute_screen_capture_fp(self, exec_ctx):
        path = exec_ctx.symbol_table.get("path")
        if not isinstance(path, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'capture' must be a string",
                    exec_ctx,
                )
            )
        try:
            import pyautogui  # type: ignore

            pyautogui.screenshot(path.value)
            return RTResult().success(Number.none)
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "pyautogui module not available",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(["x", "y", "w", "h", "p"])
    def execute_screen_capture_area_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        y = exec_ctx.symbol_table.get("y")
        w = exec_ctx.symbol_table.get("w")
        h = exec_ctx.symbol_table.get("h")
        p = exec_ctx.symbol_table.get("p")
        if not isinstance(x, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'capture_area' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(y, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'capture_area' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(w, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'capture_area' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(h, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Fourth argument of 'capture_area' must be a number",
                    exec_ctx,
                )
            )
        try:
            from PIL import ImageGrab  # type: ignore

            img = ImageGrab.grab(
                bbox=(
                    int(x.value),
                    int(y.value),
                    int(x.value) + int(w.value),
                    int(y.value) + int(h.value),
                )
            )
            img.save(p.value)
            return RTResult().success(Number.none)
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Pillow module not available",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(["x", "y"])
    def execute_screen_get_color_fp(self, exec_ctx):
        x = exec_ctx.symbol_table.get("x")
        y = exec_ctx.symbol_table.get("y")
        if not isinstance(x, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'get_color' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(y, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'get_color' must be a number",
                    exec_ctx,
                )
            )
        try:
            import pyautogui  # type: ignore

            color = pyautogui.screenshot().getpixel((int(x.value), int(y.value)))
            hex_color = "#%02x%02x%02x" % color
            return RTResult().success(String(hex_color))
        except ImportError:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "pyautogui module not available",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(
        ["value", "from_hex", "supress_error"], [None, Number.false, Number.false]
    )
    def execute_to_bytes(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        from_hex = exec_ctx.symbol_table.get("from_hex")
        suppress_error = exec_ctx.symbol_table.get("supress_error")

        if not isinstance(from_hex, Bool):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'to_bytes' must be a boolean (from_hex)",
                    exec_ctx,
                )
            )

        if not isinstance(suppress_error, Bool):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'to_bytes' must be a boolean (supress_error)",
                    exec_ctx,
                )
            )

        from_hex_ = bool(from_hex.value)
        suppress_error_ = bool(suppress_error.value)

        try:

            if isinstance(value, Number):
                hex_str = hex(int(value.value))[2:]
                if len(hex_str) % 2 != 0:
                    hex_str = "0" + hex_str
                return RTResult().success(Bytes(bytes.fromhex(hex_str)))

            elif isinstance(value, String):
                if from_hex_:
                    return RTResult().success(Bytes(bytes.fromhex(value.value)))
                else:
                    return RTResult().success(Bytes(value.value.encode()))

            elif isinstance(value, List):
                byte_values = []
                for i, element in enumerate(value.value):
                    if not isinstance(element, Number):
                        return RTResult().failure(
                            TError(
                                self.pos_start,
                                self.pos_end,
                                f"First argument of 'to_bytes' must be a list of numbers",
                                exec_ctx,
                            )
                        )

                    num_val = int(element.value)
                    if not (0 <= num_val <= 255):
                        return RTResult().failure(
                            RTError(
                                self.pos_start,
                                self.pos_end,
                                f"Byte value must be between 0 and 255 (found {num_val} at index {i})",
                                exec_ctx,
                            )
                        )
                    byte_values.append(num_val)

                return RTResult().success(Bytes(bytes(byte_values)))

            elif isinstance(value, Bytes):
                return RTResult().success(Bytes(value.value))

            else:
                raise TypeError(f"Can't convert type '{value.type()}' to bytes")

        except Exception as e:
            if suppress_error_:
                return RTResult().success(Number.none)
            else:
                return RTResult().failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        f"Failed to convert value of type '{value.type()}' to bytes: {e}",
                        exec_ctx,
                    )
                )

    @set_args(["value"])
    def execute_is_bytes(self, exec_ctx):
        is_bytes = isinstance(exec_ctx.symbol_table.get("value"), Bytes)
        return RTResult().success(Number.true if is_bytes else Number.false)

    @set_args(["s", "encoding", "errors"], [None, String("utf-8"), String("strict")])
    def execute_decode_fp(self, exec_ctx):
        s = exec_ctx.symbol_table.get("s")
        encoding = exec_ctx.symbol_table.get("encoding")
        errors = exec_ctx.symbol_table.get("errors")
        if not isinstance(s, Bytes):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'decode' must be bytes",
                    exec_ctx,
                )
            )
        if not isinstance(encoding, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'decode' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(errors, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'decode' must be a string",
                    exec_ctx,
                )
            )
        try:
            decoded = s.value.decode(encoding.value, errors.value)
            return RTResult().success(String(decoded))
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to decode bytes: {e}",
                    exec_ctx,
                )
            )

    @set_args(["s", "encoding", "errors"], [None, String("utf-8"), String("strict")])
    def execute_encode_fp(self, exec_ctx):
        s = exec_ctx.symbol_table.get("s")
        encoding = exec_ctx.symbol_table.get("encoding")
        errors = exec_ctx.symbol_table.get("errors")
        if not isinstance(s, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'encode' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(encoding, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'encode' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(errors, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'encode' must be a string",
                    exec_ctx,
                )
            )
        try:
            encoded = s.value.encode(encoding.value, errors.value)
            return RTResult().success(Bytes(encoded))
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to encode string: {e}",
                    exec_ctx,
                )
            )

    @set_args(["value"])
    def execute_is_py_obj(self, exec_ctx):
        is_py_obj = isinstance(exec_ctx.symbol_table.get("value"), PyObject)
        return RTResult().success(Number.true if is_py_obj else Number.false)

    @set_args(["value"])
    def execute_is_namespace(self, exec_ctx):
        is_namespace = isinstance(exec_ctx.symbol_table.get("value"), NameSpace)
        return RTResult().success(Number.true if is_namespace else Number.false)

    @set_args(["value"])
    def execute_is_thread_pool(self, exec_ctx):
        is_thread_pool = isinstance(exec_ctx.symbol_table.get("value"), ThreadPool)
        return RTResult().success(Number.true if is_thread_pool else Number.false)

    @set_args(["value"])
    def execute_is_future(self, exec_ctx):
        is_future = isinstance(exec_ctx.symbol_table.get("value"), Future)
        return RTResult().success(Number.true if is_future else Number.false)

    @set_args(["value"])
    def execute_is_nan(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        if not isinstance(value, Number):
            return RTResult().success(Number.false)
        if math.isnan(value.value):
            return RTResult().success(Number.true)
        else:
            return RTResult().success(Number.false)

    @set_args(["value"])
    def execute_parse_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        if not isinstance(value, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'parse' must be a string",
                    exec_ctx,
                )
            )
        try:
            parsed = json.loads(value.value)
            return RTResult().success(self.validate_pyexec_result(parsed))
        except json.JSONDecodeError as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to parse JSON: {e}",
                    exec_ctx,
                )
            )

    @set_args(["value"])
    def execute_stringify_fp(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        try:
            stringified = json.dumps(self.convert_zer_to_py(value))
            return RTResult().success(String(stringified))
        except (TypeError, OverflowError) as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Failed to stringify to JSON: {e}",
                    exec_ctx,
                )
            )

    @set_args(["channel", "value"])
    def execute_channel_send_fp(self, exec_ctx):
        channel = exec_ctx.symbol_table.get("channel")
        value = exec_ctx.symbol_table.get("value")
        if not isinstance(channel, Channel):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'send' must be a channel",
                    exec_ctx,
                )
            )

        channel.queue.put(value)
        return RTResult().success(Number.none)

    @set_args(["channel"])
    def execute_channel_receive_fp(self, exec_ctx):
        channel = exec_ctx.symbol_table.get("channel")
        if not isinstance(channel, Channel):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'receive' must be a channel",
                    exec_ctx,
                )
            )

        try:
            value = channel.queue.get()
            return RTResult().success(value)
        except Exception as e:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Error receiving from channel: {e}",
                    exec_ctx,
                )
            )

    @set_args(["channel"])
    def execute_channel_is_empty_fp(self, exec_ctx):
        channel = exec_ctx.symbol_table.get("channel")
        if not isinstance(channel, Channel):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'is_empty' must be a channel",
                    exec_ctx,
                )
            )
        return RTResult().success(Bool(channel.queue.empty()))

    @set_args([])
    def execute_channel_new_fp(self, _):
        channel = Channel(PyQueue())
        return RTResult().success(channel)

    @set_args(
        ["value1", "value2", "rel_tol", "abs_tol"],
        [None, None, Number(1e-9), Number(0.0)],
    )
    def execute_is_close_fp(self, exec_ctx):
        v1 = exec_ctx.symbol_table.get("value1").value
        v2 = exec_ctx.symbol_table.get("value2").value
        rel_tol = exec_ctx.symbol_table.get("rel_tol").value
        abs_tol = exec_ctx.symbol_table.get("abs_tol").value

        return RTResult().success(
            Bool(math.isclose(v1, v2, rel_tol=rel_tol, abs_tol=abs_tol))
        )

    @set_args(["value"])
    def execute_is_channel(self, exec_ctx):
        is_channel = isinstance(exec_ctx.symbol_table.get("value"), Channel)
        return RTResult().success(Number.true if is_channel else Number.false)

    @set_args(["value"])
    def execute_is_cfloat(self, exec_ctx):
        is_cfloat = isinstance(exec_ctx.symbol_table.get("value"), CFloat)
        return RTResult().success(Number.true if is_cfloat else Number.false)

    @set_args(["value", "supress_error"], [None, Bool.false])
    def execute_to_cfloat(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        supress_error = exec_ctx.symbol_table.get("supress_error")

        if not isinstance(supress_error, Bool):
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'to_cfloat' must be a boolean",
                    exec_ctx,
                )
            )

        supress_error_ = bool(supress_error.value)

        try:
            if isinstance(value, CFloat):
                result = CFloat(value.value)
                return RTResult().success(result)

            elif isinstance(value, Number):
                decimal_value = Fraction(str(value.value))
                result = CFloat(decimal_value)
                return RTResult().success(result)

            elif isinstance(value, String):
                try:
                    decimal_value = Fraction(value.value)
                except ZeroDivisionError:
                    return RTResult().failure(
                        RTError(
                            self.pos_start,
                            self.pos_end,
                            "Division by zero",
                            exec_ctx,
                        )
                    )
                result = CFloat(decimal_value)
                return RTResult().success(result)

            else:
                if supress_error_:
                    result = CFloat(Fraction("0"))
                    return RTResult().success(result)
                else:
                    return RTResult().failure(
                        RTError(
                            self.pos_start,
                            self.pos_end,
                            f"Can't convert '{value.type()}' to decimal",
                            exec_ctx,
                        )
                    )

        except (ValueError, TypeError) as e:
            if supress_error_:
                result = CFloat(Fraction("0"))
                return RTResult().success(result)
            else:
                return RTResult().failure(
                    RTError(
                        self.pos_start,
                        self.pos_end,
                        f"Failed to convert to decimal: {str(e)}",
                        exec_ctx,
                    )
                )

    @set_args(["max_workers"], [Number(5)])
    def execute_thread_pool_new_fp(self, exec_ctx):
        max_workers = exec_ctx.symbol_table.get("max_workers")
        if not isinstance(max_workers, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'new' must be a number",
                    exec_ctx,
                )
            )
        return RTResult().success(ThreadPool(max_workers.value))

    @set_args(["pool", "func", "args", "kwargs"], [None, None, List([]), HashMap({})])
    def execute_thread_pool_submit_fp(self, exec_ctx):
        pool = exec_ctx.symbol_table.get("pool")
        func = exec_ctx.symbol_table.get("func")
        args = exec_ctx.symbol_table.get("args")
        kwargs = exec_ctx.symbol_table.get("kwargs")

        if not isinstance(pool, ThreadPool):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'submit' must be a thread pool",
                    exec_ctx,
                )
            )
        if not isinstance(func, BaseFunction):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'submit' must be a function",
                    exec_ctx,
                )
            )
        if not isinstance(args, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'submit' must be a list",
                    exec_ctx,
                )
            )
        if not isinstance(kwargs, HashMap):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Fourth argument of 'submit' must be a hashmap",
                    exec_ctx,
                )
            )

        positional_args = args.value
        keyword_args = {
            k.value: v for k, v in kwargs.value.items() if hasattr(k, "value")
        }

        def task_wrapper():
            res = func.execute(positional_args, keyword_args)

            if res.error:
                raise ThreadPoolError(res.error)
            return res.value

        future = pool.executor.submit(task_wrapper)
        return RTResult().success(Future(future))

    @set_args(["pool", "wait"], [None, Bool.true])
    def execute_thread_pool_shutdown_fp(self, exec_ctx):
        pool = exec_ctx.symbol_table.get("pool")
        wait = exec_ctx.symbol_table.get("wait")

        if not isinstance(pool, ThreadPool):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'shutdown' must be a thread pool",
                    exec_ctx,
                )
            )
        if not isinstance(wait, Bool):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'shutdown' must be a boolean",
                    exec_ctx,
                )
            )

        pool.executor.shutdown(wait=wait.value)
        return RTResult().success(Number.none)

    @set_args(["future"])
    def execute_future_result_fp(self, exec_ctx):
        future_obj = exec_ctx.symbol_table.get("future")
        if not isinstance(future_obj, Future):
            return RTResult().failure(
                TError(
                    self.pos_start, self.pos_end, "Argument must be a future", exec_ctx
                )
            )

        try:
            result = future_obj.future.result()
            return RTResult().success(result)
        except ThreadPoolError as e:
            return RTResult().failure(e.err)
        except Exception as err:
            return RTResult().failure(
                RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Unexpected Python error in 'result': {err}",
                    exec_ctx,
                )
            )

    @set_args(["future"])
    def execute_future_done_fp(self, exec_ctx):
        future_obj = exec_ctx.symbol_table.get("future")
        if not isinstance(future_obj, Future):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'is_done' must be a future",
                    exec_ctx,
                )
            )
        return RTResult().success(Bool(future_obj.future.done()))

    @set_args(["message", "title"])
    def execute_msgbox_alert_fp(self, exec_ctx):
        msg = exec_ctx.symbol_table.get("message")
        title = exec_ctx.symbol_table.get("title")

        if not isinstance(msg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'alert' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(title, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'alert' must be a string",
                    exec_ctx,
                )
            )

        try:
            import pyautogui  # type: ignore

            result = pyautogui.alert(str(msg.value), str(title.value))
            return RTResult().success(Number.none)
        except Exception as e:
            return RTResult().failure(
                TError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(
        ["message", "title", "buttons"],
        [None, None, List([String("Ok"), String("Cancel")])],
    )
    def execute_msgbox_confirm_fp(self, exec_ctx):
        msg = exec_ctx.symbol_table.get("message")
        title = exec_ctx.symbol_table.get("title")
        buttons = exec_ctx.symbol_table.get("buttons")

        if not isinstance(msg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'confirm' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(title, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'confirm' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(buttons, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Third argument of 'confirm' must be a list",
                    exec_ctx,
                )
            )

        try:
            import pyautogui  # type: ignore

            result = pyautogui.confirm(
                str(msg.value),
                str(title.value),
                [str(b.value) for b in buttons.value if isinstance(b, String)],
            )
            return RTResult().success(String(result if result else Number.none))
        except Exception as e:
            return RTResult().failure(
                TError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(["message", "title"])
    def execute_msgbox_prompt_fp(self, exec_ctx):
        msg = exec_ctx.symbol_table.get("message")
        title = exec_ctx.symbol_table.get("title")

        if not isinstance(msg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'prompt' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(title, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'prompt' must be a string",
                    exec_ctx,
                )
            )

        try:
            import pyautogui  # type: ignore

            result = pyautogui.prompt(str(msg.value), str(title.value))
            return RTResult().success(String(result if result else Number.none))
        except Exception as e:
            return RTResult().failure(
                TError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(["message", "title"])
    def execute_msgbox_password_fp(self, exec_ctx):
        msg = exec_ctx.symbol_table.get("message")
        title = exec_ctx.symbol_table.get("title")

        if not isinstance(msg, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'password' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(title, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'password' must be a string",
                    exec_ctx,
                )
            )

        try:
            import pyautogui  # type: ignore

            result = pyautogui.password(str(msg.value), str(title.value))
            return RTResult().success(String(result if result else Number.none))
        except Exception as e:
            return RTResult().failure(
                TError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args([])
    def execute_datetime_now_fp(self, exec_ctx):
        try:
            result = datetime.now().isoformat(" ")
            return RTResult().success(String(result))
        except Exception as e:
            return RTResult().failure(
                TError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args([])
    def execute_date_today_fp(self, exec_ctx):
        try:
            result = date.today().isoformat()
            return RTResult().success(String(result))
        except Exception as e:
            return RTResult().failure(
                TError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(["fmt"])
    def execute_datetime_format_fp(self, exec_ctx):
        fmt = exec_ctx.symbol_table.get("fmt")
        if not isinstance(fmt, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'format' must be a string",
                    exec_ctx,
                )
            )
        try:
            result = datetime.now().strftime(fmt.value)
            return RTResult().success(String(result))
        except Exception as e:
            return RTResult().failure(
                TError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(["s", "fmt"])
    def execute_datetime_parse_fp(self, exec_ctx):
        s = exec_ctx.symbol_table.get("s")
        fmt = exec_ctx.symbol_table.get("fmt")
        if not isinstance(s, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'parse' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(fmt, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'parse' must be a string",
                    exec_ctx,
                )
            )
        try:
            dt = datetime.strptime(s.value, fmt.value)
            return RTResult().success(String(dt.isoformat(" ")))
        except Exception as e:
            return RTResult().failure(
                TError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(["days"])
    def execute_datetime_add_days_fp(self, exec_ctx):
        days = exec_ctx.symbol_table.get("days")
        if not isinstance(days, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'add_days' must be a number",
                    exec_ctx,
                )
            )
        try:
            new_dt = datetime.now() + timedelta(days=int(days.value))
            return RTResult().success(String(new_dt.isoformat(" ")))
        except Exception as e:
            return RTResult().failure(
                TError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(["dt1", "dt2"])
    def execute_datetime_diff_fp(self, exec_ctx):
        dt1 = exec_ctx.symbol_table.get("dt1")
        dt2 = exec_ctx.symbol_table.get("dt2")
        if not isinstance(dt1, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'diff' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(dt2, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'diff' must be a string",
                    exec_ctx,
                )
            )
        try:
            d1 = datetime.fromisoformat(dt1.value)
            d2 = datetime.fromisoformat(dt2.value)
            delta = d1 - d2
            return RTResult().success(Number(delta.days))
        except Exception as e:
            return RTResult().failure(
                TError(self.pos_start, self.pos_end, str(e), exec_ctx)
            )

    @set_args(["str"], vargs_name="lst")
    def execute_string_format_fp(self, exec_ctx):
        _str = exec_ctx.symbol_table.get("str")
        lst = exec_ctx.symbol_table.get("lst")

        if not isinstance(_str, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'format' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(lst, List):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'format' must be a list",
                    exec_ctx,
                )
            )
        r = _str.value.format(*lst.value)
        return RTResult().success(String(r))

    @set_args(["value"])
    def execute_clone(
        self, exec_ctx
    ):  # This may cause lag if overused, and should only be used for functions or namespaces when truly needed
        value = exec_ctx.symbol_table.get("value")
        return RTResult().success(deepcopy(value))

    @set_args(["a", "b"])
    def execute_shl(self, exec_ctx):
        a = exec_ctx.symbol_table.get("a")
        b = exec_ctx.symbol_table.get("b")
        if not isinstance(a, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'shl' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(b, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'shl' must be a number",
                    exec_ctx,
                )
            )
        return RTResult().success(Number(int(a.value) << int(b.value)))

    @set_args(["a", "b"])
    def execute_shr(self, exec_ctx):
        a = exec_ctx.symbol_table.get("a")
        b = exec_ctx.symbol_table.get("b")
        if not isinstance(a, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'shr' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(b, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'shr' must be a number",
                    exec_ctx,
                )
            )
        return RTResult().success(Number(int(a.value) >> int(b.value)))

    @set_args(["a", "b"])
    def execute_bitwise_and(self, exec_ctx):
        a = exec_ctx.symbol_table.get("a")
        b = exec_ctx.symbol_table.get("b")
        if not isinstance(a, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'bitwise_and' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(b, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'bitwise_and' must be a number",
                    exec_ctx,
                )
            )
        return RTResult().success(Number(int(a.value) & int(b.value)))

    @set_args(["a", "b"])
    def execute_bitwise_or(self, exec_ctx):
        a = exec_ctx.symbol_table.get("a")
        b = exec_ctx.symbol_table.get("b")
        if not isinstance(a, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'bitwise_or' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(b, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'bitwise_or' must be a number",
                    exec_ctx,
                )
            )
        return RTResult().success(Number(int(a.value) | int(b.value)))

    @set_args(["a", "b"])
    def execute_bitwise_xor(self, exec_ctx):
        a = exec_ctx.symbol_table.get("a")
        b = exec_ctx.symbol_table.get("b")
        if not isinstance(a, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'bitwise_xor' must be a number",
                    exec_ctx,
                )
            )
        if not isinstance(b, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'bitwise_xor' must be a number",
                    exec_ctx,
                )
            )
        return RTResult().success(Number(int(a.value) ^ int(b.value)))

    @set_args(["a"])
    def execute_bitwise_not(self, exec_ctx):
        a = exec_ctx.symbol_table.get("a")
        if not isinstance(a, Number):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'bitwise_not' must be a number",
                    exec_ctx,
                )
            )
        return RTResult().success(Number(~int(a.value)))

    @set_args(["file_path"])
    def execute_read_csv_fp(self, exec_ctx):
        file_path_obj = exec_ctx.symbol_table.get("file_path")
        if not isinstance(file_path_obj, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'read' must be a string",
                    exec_ctx,
                )
            )

        try:
            file_path = file_path_obj.value
            with open(file_path, mode="r", newline="", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)

                try:
                    header = next(reader)
                except StopIteration:
                    return RTResult().success(HashMap({}))

                py_data = {col_name: [] for col_name in header}

                for row in reader:
                    if len(row) == len(header):
                        for col_name, cell_value in zip(header, row):
                            py_data[col_name].append(cell_value)

            zyx_hashmap = self.validate_pyexec_result(py_data)
            return RTResult().success(zyx_hashmap)

        except FileNotFoundError:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"File not found: '{file_path_obj.value}'",
                    exec_ctx,
                )
            )
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Error reading CSV file: {e}",
                    exec_ctx,
                )
            )

    @set_args(["file_path", "data"])
    def execute_write_csv_fp(self, exec_ctx):
        file_path_obj = exec_ctx.symbol_table.get("file_path")
        data_obj = exec_ctx.symbol_table.get("data")

        if not isinstance(file_path_obj, String):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "First argument of 'write' must be a string",
                    exec_ctx,
                )
            )
        if not isinstance(data_obj, HashMap):
            return RTResult().failure(
                TError(
                    self.pos_start,
                    self.pos_end,
                    "Second argument of 'write' must be a hashmap",
                    exec_ctx,
                )
            )

        try:
            py_data = self.convert_zer_to_py(data_obj)

            if not py_data:
                open(file_path_obj.value, "w").close()
                return RTResult().success(Number.none)

            columns = list(py_data.values())
            if columns:
                num_rows = len(columns[0])
                for col in columns[1:]:
                    if len(col) != num_rows:
                        return RTResult().failure(
                            RTError(
                                self.pos_start,
                                self.pos_end,
                                "All columns in the hashmap must have the same number of rows",
                                exec_ctx,
                            )
                        )

            header = list(py_data.keys())
            rows_to_write = zip(*py_data.values())

            with open(
                file_path_obj.value, mode="w", newline="", encoding="utf-8"
            ) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                writer.writerows(rows_to_write)

            return RTResult().success(Number.none)
        except Exception as e:
            return RTResult().failure(
                IError(
                    self.pos_start,
                    self.pos_end,
                    f"Error writing to CSV file: {e}",
                    exec_ctx,
                )
            )


for method_name in [m for m in dir(BuiltInFunction) if m.startswith("execute_")]:
    func_name = method_name[8:]
    method = getattr(BuiltInFunction, method_name)
    if hasattr(method, "arg_names"):
        setattr(BuiltInFunction, func_name, BuiltInFunction(func_name))
        BUILTIN_FUNCTIONS.append(func_name)


class StaticScope:
    def __init__(self, parent=None, is_global=False):
        self.parent = parent
        self.is_global = is_global
        self.locals = []
        self.using = set()
        self.nonlocals = set()

    def define_local(self, name):
        if name not in self.locals:
            self.locals.append(name)
        return self.locals.index(name)

    def resolve(self, name):
        if name in self.locals:
            return ("local", self.locals.index(name), name)
        if name in self.nonlocals:
            depth = 1
            curr = self.parent
            while curr:
                if name in curr.locals:
                    return ("nonlocal", depth, curr.locals.index(name), name)
                depth += 1
                curr = curr.parent
            return ("global", name)
        if name in self.using or self.is_global:
            return ("global", name)

        depth = 1
        curr = self.parent
        while curr:
            if name in curr.locals:
                return ("nonlocal", depth, curr.locals.index(name), name)
            if curr.is_global:
                return ("global", name)
            depth += 1
            curr = curr.parent

        return ("global", name)


class ASTCompiler:
    def __init__(self):
        self.scope_stack = [StaticScope(is_global=True)]

    def compile(self, node):
        if node is None:
            return None
        if isinstance(node, list):
            compiled_list = []
            for n in node:
                compiled_list.append(self.compile(n))
            return compiled_list
        if isinstance(node, tuple):
            return tuple(self.compile(n) for n in node)

        node_type = type(node).__name__
        if not node_type.endswith("Node"):
            return node

        if node_type == "FuncDefNode":
            return self.compile_FuncDefNode(node)
        elif node_type == "VarAssignNode":
            return self.compile_VarAssignNode(node)
        elif node_type == "VarAccessNode":
            return self.compile_VarAccessNode(node)
        elif node_type == "UsingNode":
            return self.compile_UsingNode(node)
        elif node_type == "UsingParentNode":
            return self.compile_UsingParentNode(node)
        elif node_type == "DelNode":
            return self.compile_DelNode(node)
        elif node_type == "ForNode":
            return self.compile_ForNode(node)
        elif node_type == "ForInNode":
            return self.compile_ForInNode(node)
        elif node_type == "NameSpaceNode":
            return self.compile_NameSpaceNode(node)

        keys = (
            node.__slots__ if hasattr(node, "__slots__") else list(node.__dict__.keys())
        )
        compiled_attrs = [node_type]
        for key in keys:
            compiled_attrs.append(self.compile(getattr(node, key, None)))
        return tuple(compiled_attrs)

    def compile_NameSpaceNode(self, node):
        new_scope = StaticScope(parent=self.scope_stack[-1], is_global=True)
        self.scope_stack.append(new_scope)
        compiled_stmts = self.compile(node.statements)
        self.scope_stack.pop()
        return (
            "NameSpaceNode",
            node.namespace_name,
            compiled_stmts,
            node.pos_start,
            node.pos_end,
        )

    def compile_FuncDefNode(self, node):
        func_name_tok = node.var_name_tok
        func_addr = None
        if func_name_tok:
            name = func_name_tok.value
            scope = self.scope_stack[-1]
            if (
                name not in scope.locals
                and name not in scope.using
                and name not in scope.nonlocals
            ):
                if scope.is_global:
                    func_addr = ("global", name)
                else:
                    idx = scope.define_local(name)
                    func_addr = ("local", idx, name)
            else:
                func_addr = scope.resolve(name)

        parent_scope = self.scope_stack[-1]
        new_scope = StaticScope(parent=parent_scope)
        self.scope_stack.append(new_scope)

        arg_names = [arg.value for arg in node.arg_name_toks]
        for name in arg_names:
            new_scope.define_local(name)
        if node.vargs_name_tok:
            new_scope.define_local(node.vargs_name_tok.value)
        if node.kargs_name_tok:
            new_scope.define_local(node.kargs_name_tok.value)

        compiled_body = self.compile(node.body_node)
        num_locals = len(new_scope.locals)
        self.scope_stack.pop()

        return (
            "FuncDefNode",
            func_addr,
            node.arg_name_toks,
            self.compile(node.defaults),
            node.vargs_name_tok,
            node.kargs_name_tok,
            compiled_body,
            node.should_auto_return,
            self.compile(node.decorator_nodes),
            num_locals,
            node.pos_start,
            node.pos_end,
        )

    def compile_VarAssignNode(self, node):
        name = node.var_name_tok.value
        scope = self.scope_stack[-1]

        if (
            name not in scope.locals
            and name not in scope.using
            and name not in scope.nonlocals
        ):
            if scope.is_global:
                addr = ("global", name)
            else:
                idx = scope.define_local(name)
                addr = ("local", idx, name)
        else:
            addr = scope.resolve(name)

        return (
            "ResolvedVarAssign",
            addr,
            self.compile(node.value_node),
            node.pos_start,
            node.pos_end,
        )

    def compile_VarAccessNode(self, node):
        name = node.var_name_tok.value
        addr = self.scope_stack[-1].resolve(name)
        return ("ResolvedVarAccess", addr, node.pos_start, node.pos_end)

    def compile_UsingNode(self, node):
        for tok in node.var_name_toks:
            self.scope_stack[-1].using.add(tok.value)
        return ("NoOp",)

    def compile_UsingParentNode(self, node):
        for tok in node.var_name_toks:
            self.scope_stack[-1].nonlocals.add(tok.value)
        return ("NoOp",)

    def compile_DelNode(self, node):
        addrs = []
        for tok in node.var_name_toks:
            addrs.append(self.scope_stack[-1].resolve(tok.value))
        return ("ResolvedDel", addrs, node.pos_start, node.pos_end)

    def compile_ForNode(self, node):
        var_name = node.var_name_tok.value
        scope = self.scope_stack[-1]
        if (
            var_name not in scope.locals
            and var_name not in scope.using
            and var_name not in scope.nonlocals
        ):
            if scope.is_global:
                addr = ("global", var_name)
            else:
                idx = scope.define_local(var_name)
                addr = ("local", idx, var_name)
        else:
            addr = scope.resolve(var_name)

        return (
            "ForNode",
            addr,
            self.compile(node.start_value_node),
            self.compile(node.end_value_node),
            self.compile(node.step_value_node),
            self.compile(node.body_node),
            node.should_return_none,
            node.pos_start,
            node.pos_end,
        )

    def compile_ForInNode(self, node):
        scope = self.scope_stack[-1]
        var_addrs = []
        for tok in node.var_name_toks:
            name = tok.value
            if (
                name not in scope.locals
                and name not in scope.using
                and name not in scope.nonlocals
            ):
                if scope.is_global:
                    addr = ("global", name)
                else:
                    idx = scope.define_local(name)
                    addr = ("local", idx, name)
            else:
                addr = scope.resolve(name)
            var_addrs.append(addr)

        return (
            "ForInNode",
            var_addrs,
            self.compile(node.iterable_node),
            self.compile(node.body_node),
            node.pos_start,
            node.pos_end,
            node.should_return_none,
        )


class Interpreter:
    _visit_table = None
    _COMP_OP_MAP = {
        TT_EE: "get_comparison_eq",
        TT_NE: "get_comparison_ne",
        TT_LT: "get_comparison_lt",
        TT_GT: "get_comparison_gt",
        TT_LTE: "get_comparison_lte",
        TT_GTE: "get_comparison_gte",
    }
    _BIN_OP_MAP = {
        TT_PLUS: "added_to",
        TT_MINUS: "subbed_by",
        TT_MUL: "multed_by",
        TT_DIV: "dived_by",
        TT_POW: "powed_by",
        TT_MOD: "moduled_by",
        TT_EE: "get_comparison_eq",
        TT_NE: "get_comparison_ne",
        TT_LT: "get_comparison_lt",
        TT_GT: "get_comparison_gt",
        TT_LTE: "get_comparison_lte",
        TT_GTE: "get_comparison_gte",
        TT_FLOORDIV: "floordived_by",
        TT_DOLLAR: "dollared_by",
    }

    def __init__(self):
        if Interpreter._visit_table is None:
            table = {}
            for attr_name in dir(self.__class__):
                if attr_name.startswith("visit_") and attr_name != "visit":
                    method = getattr(self.__class__, attr_name)
                    if callable(method):
                        node_type = attr_name[len("visit_") :]
                        table[node_type] = method
            Interpreter._visit_table = table

    def visit(self, node, context):
        node_type = node[0]
        method = self._visit_table.get(node_type)
        if method is None:
            raise Exception(f"No visit method defined for {node_type}")
        return method(self, node, context)

    def assign_by_addr(self, addr, value, context):
        addr_type = addr[0]
        if addr_type == "local":
            context.locals_stack[addr[1]] = value
        elif addr_type == "nonlocal":
            depth, idx = addr[1], addr[2]
            curr = context
            for _ in range(depth):
                curr = curr.parent
            curr.locals_stack[idx] = value
        else:
            name = addr[1]
            if name in context.using_vars:
                global_st = context.symbol_table
                while global_st.parent:
                    global_st = global_st.parent
                global_st.set(name, value)
            else:
                context.symbol_table.set(name, value)
            context.private_symbol_table.set(name, value)

    def delete_by_addr(self, addr, context):
        addr_type = addr[0]
        name = addr[-1]
        if addr_type == "local":
            context.locals_stack[addr[1]] = Number.none
        elif addr_type == "nonlocal":
            depth, idx = addr[1], addr[2]
            curr = context
            for _ in range(depth):
                curr = curr.parent
            curr.locals_stack[idx] = Number.none
        else:
            context.symbol_table.remove(name)
            context.private_symbol_table.remove(name)

    def visit_NoOp(self, _, __):
        return RTResult().success(Number.none)

    def visit_ResolvedVarAccess(self, node, context):
        _, addr, pos_start, pos_end = node
        res = RTResult()
        addr_type = addr[0]
        if addr_type == "local":
            val = context.locals_stack[addr[1]]
        elif addr_type == "nonlocal":
            depth, idx = addr[1], addr[2]
            curr = context
            for _ in range(depth):
                curr = curr.parent
            val = curr.locals_stack[idx]
        else:
            name = addr[1]
            val = context.symbol_table.get(name)
            if val is None:
                val = context.private_symbol_table.get(name)

        if val is None:
            val = global_symbol_table.get(addr[1])

        if val is None:
            return res.failure(
                RTError(pos_start, pos_end, f"'{addr[1]}' is not defined", context)
            )

        copied_value = (
            val.copy() if not isinstance(val, (NameSpace, List, HashMap)) else val
        )
        copied_value = copied_value.set_pos(pos_start, pos_end).set_context(context)
        return res.success(copied_value)

    def visit_ResolvedVarAssign(self, node, context):
        _, addr, value_node, pos_start, pos_end = node
        res = RTResult()
        value = res.register(self.visit(value_node, context))
        if res.should_return():
            return res

        self.assign_by_addr(addr, value, context)
        return res.success(value)

    def visit_ResolvedDel(self, node, context):
        _, addrs, pos_start, pos_end = node
        res = RTResult()
        for addr in addrs:
            self.delete_by_addr(addr, context)
        return res.success(Number.none)

    def visit_NumberNode(self, node, context: Context):
        _, tok, pos_start, pos_end = node
        return RTResult().success(
            Number(tok.value).set_context(context).set_pos(pos_start, pos_end)
        )

    def visit_StringNode(self, node, context: Context):
        _, tok, pos_start, pos_end = node
        return RTResult().success(
            String(tok.value).set_context(context).set_pos(pos_start, pos_end)
        )

    def visit_ListNode(self, node, context: Context):
        _, element_nodes, pos_start, pos_end = node
        res = RTResult()
        value = []
        for element_node in element_nodes:
            value.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res
        return res.success(List(value).set_context(context).set_pos(pos_start, pos_end))

    def initialize_namespace(self, namespace_obj):
        if namespace_obj.get("initialized_", checked=True).value:
            return
        stmts = namespace_obj.get("statements_", checked=True)
        ns_context = namespace_obj.get("context_", checked=True)
        for stmt in stmts:
            _ = self.visit(stmt, ns_context)
        for k, v in ns_context.symbol_table.symbols.items():
            namespace_obj.set(k, v)
        for k, v in ns_context.private_symbol_table.symbols.items():
            namespace_obj.set(k, v)
        namespace_obj.set("initialized_", Number.true, checked=True)

    def visit_NameSpaceNode(self, node, context):
        _, namespace_name, statements, pos_start, pos_end = node
        res = RTResult()
        namespace = NameSpace(namespace_name)
        namespace.set_pos(pos_start, pos_end)
        namespace.set_context(context)
        ns_context = Context(namespace_name, context, pos_start)
        ns_context.symbol_table = SymbolTable(context.symbol_table)
        ns_context.private_symbol_table = SymbolTable(context.private_symbol_table)

        stmts = statements
        if isinstance(stmts, tuple) and stmts[0] == "ListNode":
            stmts = stmts[1]

        namespace.set("statements_", stmts, checked=True)
        namespace.set("context_", ns_context, checked=True)
        context.symbol_table.set(namespace_name, namespace)
        context.private_symbol_table.set(namespace_name, namespace)
        return res.success(namespace)

    def visit_MemberAccessNode(self, node, context):
        _, object_node, member_name, pos_start, pos_end = node
        res = RTResult()
        obj = res.register(self.visit(object_node, context))
        if res.should_return():
            return res
        if not isinstance(obj, NameSpace):
            return res.failure(
                TError(pos_start, pos_end, "Illegal operation -> unknown", context)
            )
        if (
            isinstance(obj, NameSpace)
            and not obj.get("initialized_", checked=True).value
        ):
            self.initialize_namespace(obj)
        member = obj.get(member_name)
        if member is None:
            return res.failure(
                RTError(
                    pos_start,
                    pos_end,
                    f"'{obj}' has no member '{member_name}'",
                    context,
                )
            )
        if isinstance(member, Error):
            return res.failure(member)
        return res.success(member)

    def visit_BinOpNode(self, node, context):
        _, left_node, op_tok, right_node, pos_start, pos_end = node
        res = RTResult()

        if op_tok.matches(TT_KEYWORD, "and"):
            left = res.register(self.visit(left_node, context))
            if res.should_return():
                return res
            if not left.is_true():
                return res.success(left)
            right = res.register(self.visit(right_node, context))
            if res.should_return():
                return res
            return res.success(right)

        if op_tok.matches(TT_KEYWORD, "or"):
            left = res.register(self.visit(left_node, context))
            if res.should_return():
                return res
            if left.is_true():
                return res.success(left)
            right = res.register(self.visit(right_node, context))
            if res.should_return():
                return res
            return res.success(right)

        left = res.register(self.visit(left_node, context))
        if res.should_return():
            return res
        right = res.register(self.visit(right_node, context))
        if res.should_return():
            return res

        op_type = op_tok.type

        if isinstance(left, Number) and isinstance(right, Number):
            if op_type == TT_PLUS:
                result = Number(left.value + right.value)
            elif op_type == TT_MINUS:
                result = Number(left.value - right.value)
            elif op_type == TT_MUL:
                result = Number(left.value * right.value)
            elif op_type == TT_DIV:
                if right.value == 0:
                    return res.failure(
                        MError(
                            right.pos_start, right.pos_end, "Division by zero", context
                        )
                    )
                result = Number(left.value / right.value)
            elif op_type == TT_MOD:
                if right.value == 0:
                    return res.failure(
                        MError(
                            right.pos_start, right.pos_end, "Division by zero", context
                        )
                    )
                result = Number(left.value % right.value)
            elif op_type == TT_FLOORDIV:
                if right.value == 0:
                    return res.failure(
                        MError(
                            right.pos_start, right.pos_end, "Division by zero", context
                        )
                    )
                result = Number(left.value // right.value)
            elif op_type == TT_POW:
                result = Number(left.value**right.value)
            else:
                result, error = getattr(left, Interpreter._COMP_OP_MAP.get(op_type))(
                    right
                )
                if error:
                    return res.failure(error)
            return res.success(result.set_pos(pos_start, pos_end))

        if isinstance(left, CFloat) and isinstance(right, CFloat):
            if op_type == TT_PLUS:
                result = CFloat(left.value + right.value)
            elif op_type == TT_MINUS:
                result = CFloat(left.value - right.value)
            elif op_type == TT_MUL:
                result = CFloat(left.value * right.value)
            elif op_type == TT_DIV:
                if right.value == 0:
                    return res.failure(
                        MError(
                            right.pos_start, right.pos_end, "Division by zero", context
                        )
                    )
                result = CFloat(left.value / right.value)
            elif op_type == TT_MOD:
                if right.value == 0:
                    return res.failure(
                        MError(
                            right.pos_start, right.pos_end, "Division by zero", context
                        )
                    )
                result = CFloat(left.value % right.value)
            elif op_type == TT_FLOORDIV:
                if right.value == 0:
                    return res.failure(
                        MError(
                            right.pos_start, right.pos_end, "Division by zero", context
                        )
                    )
                result = CFloat(left.value // right.value)
            elif op_type == TT_POW:
                result = CFloat(left.value**right.value)
            else:
                result, error = getattr(left, Interpreter._COMP_OP_MAP.get(op_type))(
                    right
                )
                if error:
                    return res.failure(error)
            return res.success(result.set_pos(pos_start, pos_end))

        if op_type in Interpreter._BIN_OP_MAP:
            method = getattr(left, Interpreter._BIN_OP_MAP[op_type])
            result, error = method(right)
        else:
            return res.failure(
                RTError(
                    pos_start, pos_end, f"Unknown binary operator '{op_tok}'", context
                )
            )

        if error:
            return res.failure(error)
        return res.success(result.set_pos(pos_start, pos_end))

    def visit_UnaryOpNode(self, node, context):
        _, op_tok, inner_node, pos_start, pos_end = node
        res = RTResult()
        value = res.register(self.visit(inner_node, context))
        if res.should_return():
            return res

        op_type = op_tok.type
        if op_type == TT_MINUS:
            result, error = value.multed_by(Number(-1))
        elif op_tok.matches(TT_KEYWORD, "not"):
            result, error = value.notted()
        else:
            return res.failure(
                RTError(
                    pos_start, pos_end, f"Unknown unary operator '{op_tok}'", context
                )
            )

        if error:
            return res.failure(error)
        return res.success(result.set_pos(pos_start, pos_end))

    def visit_IfNode(self, node, context):
        _, cases, else_case, pos_start, pos_end = node
        res = RTResult()
        for condition, expr, should_return_none in cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return():
                return res
            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return():
                    return res
                return res.success(Number.none if should_return_none else expr_value)
        if else_case:
            expr, should_return_none = else_case
            expr_value = res.register(self.visit(expr, context))
            if res.should_return():
                return res
            return res.success(Number.none if should_return_none else expr_value)
        return res.success(Number.none)

    def visit_ForNode(self, node, context):
        (
            _,
            addr,
            start_value_node,
            end_value_node,
            step_value_node,
            body_node,
            should_return_none,
            pos_start,
            pos_end,
        ) = node
        res = RTResult()
        elements = [] if not should_return_none else None

        start_value = res.register(self.visit(start_value_node, context))
        if res.should_return():
            return res
        end_value = res.register(self.visit(end_value_node, context))
        if res.should_return():
            return res
        step_value = Number(1)
        if step_value_node:
            step_value = res.register(self.visit(step_value_node, context))
            if res.should_return():
                return res

        try:
            start = int(start_value.value)
            end = int(end_value.value)
            step = int(step_value.value)
        except (ValueError, TypeError):
            return res.failure(
                RTError(
                    pos_start,
                    pos_end,
                    "Start, end, and step values for a 'for' loop must be integers",
                    context,
                )
            )

        if step == 0:
            err_pos = step_value_node[3] if step_value_node else end_value_node[3]
            return res.failure(
                RTError(
                    err_pos,
                    err_pos,
                    "Step value for a 'for' loop can't be zero",
                    context,
                )
            )

        for i in range(start, end, step):
            self.assign_by_addr(addr, Number(i), context)
            value = res.register(self.visit(body_node, context))

            if (
                res.should_return()
                and not res.loop_should_continue
                and not res.loop_should_break
            ):
                return res
            if res.loop_should_continue:
                continue
            if res.loop_should_break:
                break

            if elements is not None:
                if (
                    isinstance(value, List)
                    and body_node
                    and isinstance(body_node, tuple)
                    and body_node[0] in ("ForNode", "ForInNode")
                ):
                    elements.extend(value.value)
                else:
                    elements.append(value)

        self.delete_by_addr(addr, context)
        if should_return_none:
            return res.success(Number.none)
        else:
            return res.success(
                List(elements).set_context(context).set_pos(pos_start, pos_end)
            )

    def visit_WhileNode(self, node, context):
        _, condition_node, body_node, should_return_none, pos_start, pos_end = node
        res = RTResult()
        elements = None if should_return_none else []

        while True:
            condition = res.register(self.visit(condition_node, context))
            if res.should_return():
                return res
            if not condition.is_true():
                break

            value = res.register(self.visit(body_node, context))

            if res.should_return():
                if res.loop_should_continue:
                    continue
                if res.loop_should_break:
                    break
                return res

            if elements is not None:
                elements.append(value)

        if elements is None:
            return res.success(Number.none)
        else:
            return res.success(
                List(elements).set_context(context).set_pos(pos_start, pos_end)
            )

    def visit_FuncDefNode(self, node, context):
        (
            _,
            func_addr,
            arg_name_toks,
            defaults,
            vargs_name_tok,
            kargs_name_tok,
            body_node,
            should_auto_return,
            decorator_nodes,
            num_locals,
            pos_start,
            pos_end,
        ) = node
        res = RTResult()

        func_name = func_addr[-1] if func_addr else None
        arg_names = [arg_name.value for arg_name in arg_name_toks]

        func_value = (
            Function(
                func_name,
                body_node,
                arg_names,
                defaults,
                vargs_name_tok,
                kargs_name_tok,
                should_auto_return,
                num_locals,
            )
            .set_context(context)
            .set_pos(pos_start, pos_end)
        )

        if decorator_nodes:
            for deco_node in reversed(decorator_nodes):
                decorator = res.register(self.visit(deco_node, context))
                if res.should_return():
                    return res
                wrapped_func = res.register(decorator.execute([func_value], {}))
                if res.should_return():
                    return res
                func_value = wrapped_func

        if func_addr:
            self.assign_by_addr(func_addr, func_value, context)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        _, node_to_call, arg_nodes, pos_start, pos_end = node
        try:
            res = RTResult()
            value_to_call = res.register(self.visit(node_to_call, context))
            if res.should_return():
                return res

            value_to_call = value_to_call.copy().set_pos(pos_start, pos_end)
            value_to_call.set_context(context)
            positional_args = []
            keyword_args = {}

            for arg_node in arg_nodes:
                arg_type = arg_node[0] if isinstance(arg_node, tuple) else ""

                if arg_type == "VargsUnpackNode":
                    list_to_unpack = res.register(self.visit(arg_node[1], context))
                    if res.should_return():
                        return res
                    if not isinstance(list_to_unpack, List):
                        return res.failure(
                            RTError(
                                arg_node[2],
                                arg_node[3],
                                "Value to unpack with '*' must be a list",
                                context,
                            )
                        )
                    positional_args.extend(list_to_unpack.value)

                elif arg_type == "KargsUnpackNode":
                    map_to_unpack = res.register(self.visit(arg_node[1], context))
                    if res.should_return():
                        return res
                    if not isinstance(map_to_unpack, HashMap):
                        return res.failure(
                            RTError(
                                arg_node[2],
                                arg_node[3],
                                "Value to unpack with '**' must be a hashmap",
                                context,
                            )
                        )
                    for k, v in map_to_unpack.value.items():
                        if not isinstance(k, str):
                            return res.failure(
                                RTError(
                                    arg_node[2],
                                    arg_node[3],
                                    "Keyword argument keys must be strings",
                                    context,
                                )
                            )
                        keyword_args[k] = v

                elif arg_type == "VarAssignNode":
                    arg_name = arg_node[1].value
                    arg_value = res.register(self.visit(arg_node[2], context))
                    if res.should_return():
                        return res
                    keyword_args[arg_name] = arg_value

                else:
                    positional_args.append(res.register(self.visit(arg_node, context)))
                    if res.should_return():
                        return res

            return_value = res.register(
                value_to_call.execute(positional_args, keyword_args)
            )
            if res.should_return():
                return res

            if return_value:
                return_value = (
                    return_value.copy().set_pos(pos_start, pos_end).set_context(context)
                )

            return res.success(return_value)

        except RecursionError:
            return RTResult().failure(
                RTError(
                    pos_start,
                    pos_end,
                    f"Maximum recursion depth exceeded ({sys.getrecursionlimit()})",
                    context,
                )
            )

    def visit_ReturnNode(self, node, context):
        _, node_to_return, pos_start, pos_end = node
        res = RTResult()
        if node_to_return:
            value = res.register(self.visit(node_to_return, context))
            if res.should_return():
                return res
        else:
            value = Number.none
        return res.success_return(value)

    def visit_ContinueNode(self, _, __):
        return RTResult().success_continue()

    def visit_BreakNode(self, _, __):
        return RTResult().success_break()

    def visit_LoadNode(self, node, context: Context):
        _, module_name_tok, file_path, pos_start, pos_end = node
        res = RTResult()
        path = file_path
        if not os.path.isfile(path):
            tmp_path = os.path.join(LIBS_PATH, file_path)
            if os.path.isfile(tmp_path):
                path = os.path.join(LIBS_PATH, file_path)
            else:
                return res.failure(
                    RTError(
                        pos_start, pos_end, f"No module named '{tmp_path}'", context
                    )
                )

        result, err = load_module(path, self)
        if err:
            if isinstance(err, Error):
                return res.failure(err)
            return res.failure(RTError(pos_start, pos_end, err.error.details, context))
        return res.success(result)

    def visit_HashMapNode(self, node, context):
        _, pairs, pos_start, pos_end = node
        res = RTResult()
        result = {}
        for key_node, value_node in pairs:
            key = res.register(self.visit(key_node, context))
            if res.should_return():
                return res
            if not isinstance(key, String):
                return res.failure(
                    RTError(
                        pos_start,
                        pos_end,
                        f"Non-string key for hashmap: '{key!r}'",
                        context,
                    )
                )
            val = res.register(self.visit(value_node, context))
            if res.should_return():
                return res
            result[key.value] = val
        return res.success(HashMap(result))

    def visit_ForInNode(self, node, context: Context) -> RTResult:
        (
            _,
            var_addrs,
            iterable_node,
            body_node,
            pos_start,
            pos_end,
            should_return_none,
        ) = node
        res = RTResult()

        iterable = res.register(self.visit(iterable_node, context))
        if res.should_return():
            return res

        iterator, error = iterable.iter()
        if error:
            return res.failure(error)

        elements = [] if not should_return_none else None
        try:
            while True:
                current = next(iterator)
                if len(var_addrs) == 1:
                    self.assign_by_addr(var_addrs[0], current, context)
                else:
                    if not isinstance(current, List):
                        return res.failure(
                            RTError(
                                iterable_node[3],
                                iterable_node[4],
                                "Value to unpack must be a list",
                                context,
                            )
                        )
                    values_to_unpack = current.value
                    if len(var_addrs) != len(values_to_unpack):
                        return res.failure(
                            RTError(
                                iterable_node[3],
                                iterable_node[4],
                                f"Not enough values to unpack (expected {len(var_addrs)}, got {len(values_to_unpack)})",
                                context,
                            )
                        )
                    for i, addr in enumerate(var_addrs):
                        self.assign_by_addr(addr, values_to_unpack[i], context)

                value = res.register(self.visit(body_node, context))

                if (
                    res.should_return()
                    and not res.loop_should_continue
                    and not res.loop_should_break
                ):
                    return res
                if res.loop_should_break:
                    break
                if res.loop_should_continue:
                    continue

                if elements is not None:
                    if (
                        isinstance(value, List)
                        and body_node
                        and isinstance(body_node, tuple)
                        and body_node[0] in ("ForNode", "ForInNode")
                    ):
                        elements.extend(value.value)
                    else:
                        elements.append(value)
        except StopIteration:
            pass

        for addr in var_addrs:
            self.delete_by_addr(addr, context)

        if should_return_none:
            return res.success(Number.none)
        else:
            return res.success(
                List(elements).set_context(context).set_pos(pos_start, pos_end)
            )

    def visit_UsingNode(self, _, __):
        return RTResult().success(Number.none)

    def visit_UsingParentNode(self, _, __):
        return RTResult().success(Number.none)

    def visit_IndexAssignNode(self, node, context):
        _, obj_node, index_node, value_node, pos_start, pos_end = node
        res = RTResult()
        collection_obj = res.register(self.visit(obj_node, context))
        if res.should_return():
            return res
        index_obj = res.register(self.visit(index_node, context))
        if res.should_return():
            return res
        value_to_set = res.register(self.visit(value_node, context))
        if res.should_return():
            return res

        if isinstance(collection_obj, List):
            if not isinstance(index_obj, Number):
                return res.failure(
                    RTError(
                        index_node[3],
                        index_node[4],
                        "List index must be a number",
                        context,
                    )
                )
            idx = int(index_obj.value)
            try:
                collection_obj.value[idx] = value_to_set
            except IndexError:
                return res.failure(
                    RTError(
                        index_node[3],
                        index_node[4],
                        f"Index {idx} is out of bounds for list of size {len(collection_obj.value)}",
                        context,
                    )
                )
        elif isinstance(collection_obj, HashMap):
            if not isinstance(index_obj, String):
                return res.failure(
                    RTError(
                        index_node[3],
                        index_node[4],
                        "Hashmap key must be a string",
                        context,
                    )
                )
            key = index_obj.value
            collection_obj.value[key] = value_to_set
        else:
            return res.failure(
                RTError(
                    obj_node[3],
                    obj_node[4],
                    "Indexed assignment can only be performed on a list or hashmap",
                    context,
                )
            )

        return res.success(value_to_set)

    def visit_VargsUnpackNode(self, node, context):
        _, node_to_unpack, pos_start, pos_end = node
        return RTResult().failure(
            RTError(
                pos_start,
                pos_end,
                "Vargs unpacking (*) can only be used in function calls",
                context,
            )
        )

    def visit_KargsUnpackNode(self, node, context):
        _, node_to_unpack, pos_start, pos_end = node
        return RTResult().failure(
            RTError(
                pos_start,
                pos_end,
                "Kargs unpacking (**) can only be used in function calls",
                context,
            )
        )


global_symbol_table.set("argv_fp", List([String(e) for e in sys.argv[1:]]))
global_symbol_table.set("os_sep_fp", String(os.sep))
global_symbol_table.set("none", Number.none)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("list", String("<list>"))
global_symbol_table.set("str", String("<str>"))
global_symbol_table.set("int", String("<int>"))
global_symbol_table.set("float", String("<float>"))
global_symbol_table.set("func", String("<func>"))
global_symbol_table.set("bool", String("<bool>"))
global_symbol_table.set("hashmap", String("<hashmap>"))
global_symbol_table.set("thread", String("<thread>"))
global_symbol_table.set("bytes", String("<bytes>"))
global_symbol_table.set("py_obj", String("<py-obj>"))
global_symbol_table.set("os_name_fp", String(os.name))
global_symbol_table.set("PI_fp", Number(math.pi))
global_symbol_table.set("E_fp", Number(math.e))
global_symbol_table.set("none_type", String("<none>"))
global_symbol_table.set("cfloat", String("<cfloat>"))
global_symbol_table.set("nan", Number(float("nan")))
global_symbol_table.set("inf", Number(float("inf")))
global_symbol_table.set("neg_inf", Number(float("-inf")))
global_symbol_table.set("channel_type", String("<channel>"))
global_symbol_table.set("thread_pool_type", String("<thread-pool>"))
global_symbol_table.set("future_type", String("<future>"))

for func in BUILTIN_FUNCTIONS:
    global_symbol_table.set(func, getattr(BuiltInFunction, func))

private_symbol_table = SymbolTable()
private_symbol_table.set("is_main", Number.false)


def clean_value(value):
    if isinstance(value, List):
        cleaned_list = [
            elem for elem in value.value if not (isinstance(elem, NoneObject))
        ]

        if len(cleaned_list) == 0:
            return String("")

        return List(cleaned_list)
    return value


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    result = None
    context = None
    try:
        parser = Parser(tokens)
        ast = parser.parse()
        if ast.error:
            return None, ast.error
        interpreter = Interpreter()
        context = Context("<program>")
        context.symbol_table = global_symbol_table
        context.private_symbol_table = private_symbol_table
        context.private_symbol_table.set("is_main", Number.true)
        compiler = ASTCompiler()
        compiled_ast = compiler.compile(ast.node)
        result = interpreter.visit(compiled_ast, context)
        if fn == "<stdin>":
            value = result.value
            result.value = clean_value(value)
        else:
            result.value = ""
        return result.value, result.error
    except (KeyboardInterrupt, EOFError):
        print(
            "\n---------------------------------------------------------------------------"
        )
        print(
            "InterruptError                            Traceback (most recent call last)\n"
        )
        print(
            f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}InterruptError{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}User Terminated{Fore.RESET}{Style.RESET_ALL}"
        )
        sys.exit(2)
```

## File: `src\lexer.py`
```python
# FILE: lexer.py

from .consts import *
from .errors import ExpectedCharError, IllegalCharError, InvalidSyntaxError
from .utils import Position, Token


class Lexer:
    __slots__ = ["fn", "text", "pos", "current_char", "tokens", "open_bracket_stack"]

    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, fn, text)
        self.current_char = None
        self.advance()
        self.tokens = []
        self.open_bracket_stack = []

    def advance(self, steps=1):
        for _ in range(steps):
            self.pos.advance(self.current_char)
            self.current_char = (
                self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
            )

    def make_tokens(self):
        while self.current_char is not None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char == "#":
                self.skip_comment()
            elif self.current_char in ";\n":
                if self.open_bracket_stack:
                    self.advance()
                else:
                    if self.tokens and self.tokens[-1].type == TT_NEWLINE:
                        self.advance()
                        continue
                    newline_pos_start = self.pos.copy()
                    self.tokens.append(Token(TT_NEWLINE, pos_start=newline_pos_start))
                    self.advance()
            elif self.current_char in DIGITS:
                self.tokens.append(self.make_number())
            elif self.current_char in LETTERS + "_":
                self.tokens.append(self.make_identifier())
            elif self.current_char == '"' or self.current_char == "'":
                token, error = self.make_string()
                if error:
                    return [], error
                self.tokens.append(token)
            elif self.current_char == "+":
                self.handle_plus_or_augmented()
            elif self.current_char == "-":
                self.handle_minus_or_augmented()
            elif self.current_char == "*":
                self.handle_mul_or_dstar_or_augmented()
            elif self.current_char == "/":
                self.div_or_floordiv_or_augmented()
            elif self.current_char == "&":
                self.tokens.append(Token(TT_AND, pos_start=self.pos))
                self.advance()
            elif self.current_char == "\\":
                if self.peek_foward_steps(1) == "\n":
                    self.advance(2)
                else:
                    pos_start = self.pos.copy()
                    self.advance()
                    return [], IllegalCharError(
                        pos_start, self.pos, "Stray '\\' character in program"
                    )
            elif self.current_char == "^":
                self.handle_pow_or_augmented()
            elif self.current_char == "%":
                self.handle_mod_or_augmented()
            elif self.current_char == "=":
                self.tokens.append(self.make_equals())
            elif self.current_char == "(":
                pos_start = self.pos.copy()
                self.tokens.append(Token(TT_LPAREN, pos_start=pos_start))
                self.advance()
                self.tokens[-1].pos_end = self.pos.copy()
                self.open_bracket_stack.append((")", pos_start))
            elif self.current_char == ")":
                pos_start_closer = self.pos.copy()
                self.tokens.append(Token(TT_RPAREN, pos_start=pos_start_closer))
                self.advance()
                self.tokens[-1].pos_end = self.pos.copy()
                if not self.open_bracket_stack:
                    return [], ExpectedCharError(pos_start_closer, self.pos, "')'")
                expected_closer, _ = self.open_bracket_stack[-1]
                if expected_closer == ")":
                    self.open_bracket_stack.pop()
                else:
                    return [], ExpectedCharError(
                        pos_start_closer, self.pos, f"'{expected_closer}'"
                    )
            elif self.current_char == "[":
                pos_start = self.pos.copy()
                self.tokens.append(Token(TT_LSQUARE, pos_start=pos_start))
                self.advance()
                self.tokens[-1].pos_end = self.pos.copy()
                self.open_bracket_stack.append(("]", pos_start))
            elif self.current_char == "]":
                pos_start_closer = self.pos.copy()
                self.tokens.append(Token(TT_RSQUARE, pos_start=pos_start_closer))
                self.advance()
                self.tokens[-1].pos_end = self.pos.copy()
                if not self.open_bracket_stack:
                    return [], ExpectedCharError(pos_start_closer, self.pos, "']'")
                expected_closer, _ = self.open_bracket_stack[-1]
                if expected_closer == "]":
                    self.open_bracket_stack.pop()
                else:
                    return [], ExpectedCharError(
                        pos_start_closer, self.pos, f"'{expected_closer}'"
                    )
            elif self.current_char == "!":
                token, error = self.make_not_equals()
                if error:
                    return [], error
                self.tokens.append(token)
            elif self.current_char == "<":
                self.tokens.append(self.make_less_than())
            elif self.current_char == ">":
                self.tokens.append(self.make_greater_than())
            elif self.current_char == ".":
                self.tokens.append(Token(TT_DOT, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == ",":
                self.tokens.append(Token(TT_COMMA, pos_start=self.pos.copy()))
                self.advance()
                self.tokens[-1].pos_end = self.pos.copy()
            elif self.current_char == "{":
                pos_start = self.pos.copy()
                self.tokens.append(Token(TT_LBRACE, pos_start=pos_start))
                self.advance()
                self.tokens[-1].pos_end = self.pos.copy()
                self.open_bracket_stack.append(("}", pos_start))
            elif self.current_char == "}":
                pos_start_closer = self.pos.copy()
                self.tokens.append(Token(TT_RBRACE, pos_start=pos_start_closer))
                self.advance()
                self.tokens[-1].pos_end = self.pos.copy()
                if not self.open_bracket_stack:
                    return [], ExpectedCharError(pos_start_closer, self.pos, "'}'")
                expected_closer, _ = self.open_bracket_stack[-1]
                if expected_closer == "}":
                    self.open_bracket_stack.pop()
                else:
                    return [], ExpectedCharError(
                        pos_start_closer, self.pos, f"'{expected_closer}'"
                    )
            elif self.current_char == ":":
                pos_start = self.pos.copy()
                self.tokens.append(Token(TT_COLON, pos_start=pos_start))
                self.advance()
            elif self.current_char == "$":
                pos_start = self.pos.copy()
                self.tokens.append(Token(TT_DOLLAR, pos_start=pos_start))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        if self.open_bracket_stack:
            expected_closer, opener_pos_start = self.open_bracket_stack[-1]
            return [], ExpectedCharError(
                opener_pos_start, self.pos, f"Expected '{expected_closer}'"
            )

        self.tokens.append(Token(TT_EOF, pos_start=self.pos))
        return self.tokens, None

    def make_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()
        while self.current_char is not None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
            num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_string(self):
        quote_char = self.current_char
        return self._process_string_literal(quote_char)

    def _process_string_literal(self, quote_char):
        string_content = []
        pos_start = self.pos.copy()
        self.advance()
        is_multiline = False
        closing_sequence = quote_char
        if self.current_char == quote_char and self.peek_foward_steps(1) == quote_char:
            is_multiline = True
            closing_sequence = quote_char * 3
            self.advance(2)
        escape_character = False
        while self.current_char is not None:
            if is_multiline:
                if (
                    self.current_char == quote_char
                    and self.peek_foward_steps(1) == quote_char
                    and self.peek_foward_steps(2) == quote_char
                ):
                    self.advance(3)
                    break
            else:
                if not escape_character and self.current_char == quote_char:
                    self.advance()
                    break
            if escape_character:
                string_content.append(self.current_char)
                escape_character = False
            elif self.current_char == "\\":
                string_content.append("\\")
                escape_character = True
            else:
                string_content.append(self.current_char)
            self.advance()
        else:
            return None, ExpectedCharError(pos_start, self.pos, f"'{closing_sequence}'")
        raw_string = "".join(string_content)
        try:
            processed_string = raw_string.encode("raw_unicode_escape").decode(
                "unicode_escape"
            )
        except UnicodeDecodeError:
            return None, IllegalCharError(
                pos_start, self.pos, f"Invalid escape sequence in string"
            )
        return Token(TT_STRING, processed_string, pos_start, self.pos), None

    def peek_foward_steps(self, steps) -> str | None:
        peek_pos_idx = self.pos.idx + steps
        if 0 <= peek_pos_idx < len(self.text):
            return self.text[peek_pos_idx]
        return None

    def handle_plus_or_augmented(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == "=":
            self.advance()
            self.tokens.append(
                Token(TT_PLUSEQ, pos_start=pos_start, pos_end=self.pos.copy())
            )
        else:
            self.tokens.append(
                Token(TT_PLUS, pos_start=pos_start, pos_end=self.pos.copy())
            )

    def handle_minus_or_augmented(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == ">":
            self.advance()
            self.tokens.append(
                Token(TT_ARROW, pos_start=pos_start, pos_end=self.pos.copy())
            )
        elif self.current_char == "=":
            self.advance()
            self.tokens.append(
                Token(TT_MINUSEQ, pos_start=pos_start, pos_end=self.pos.copy())
            )
        else:
            self.tokens.append(
                Token(TT_MINUS, pos_start=pos_start, pos_end=self.pos.copy())
            )

    def handle_mul_or_dstar_or_augmented(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == "*":
            self.advance()
            self.tokens.append(
                Token(TT_DOUBLE_STAR, pos_start=pos_start, pos_end=self.pos.copy())
            )
        elif self.current_char == "=":
            self.advance()
            self.tokens.append(
                Token(TT_MULEQ, pos_start=pos_start, pos_end=self.pos.copy())
            )
        else:
            self.tokens.append(
                Token(TT_MUL, pos_start=pos_start, pos_end=self.pos.copy())
            )

    def handle_pow_or_augmented(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == "=":
            self.advance()
            self.tokens.append(
                Token(TT_POWEQ, pos_start=pos_start, pos_end=self.pos.copy())
            )
        else:
            self.tokens.append(
                Token(TT_POW, pos_start=pos_start, pos_end=self.pos.copy())
            )

    def handle_mod_or_augmented(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == "=":
            self.advance()
            self.tokens.append(
                Token(TT_MODEQ, pos_start=pos_start, pos_end=self.pos.copy())
            )
        else:
            self.tokens.append(
                Token(TT_MOD, pos_start=pos_start, pos_end=self.pos.copy())
            )

    def div_or_floordiv_or_augmented(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == "/":
            self.advance()
            if self.current_char == "=":
                self.advance()
                self.tokens.append(
                    Token(TT_FLOORDIVEQ, pos_start=pos_start, pos_end=self.pos.copy())
                )
            else:
                self.tokens.append(
                    Token(TT_FLOORDIV, pos_start=pos_start, pos_end=self.pos.copy())
                )
        elif self.current_char == "=":
            self.advance()
            self.tokens.append(
                Token(TT_DIVEQ, pos_start=pos_start, pos_end=self.pos.copy())
            )
        else:
            self.tokens.append(
                Token(TT_DIV, pos_start=pos_start, pos_end=self.pos.copy())
            )

    def make_identifier(self) -> Token:
        id_str = ""
        pos_start = self.pos.copy()
        while (
            self.current_char is not None and self.current_char in LETTERS_DIGITS + "_"
        ):
            id_str += self.current_char
            self.advance()
        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos.copy())

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == "=":
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos.copy()), None
        return None, ExpectedCharError(pos_start, self.pos.copy(), "'=' (after '!')")

    def make_equals(self) -> Token:
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == "=":
            self.advance()
            tok_type = TT_EE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())

    def make_less_than(self) -> Token:
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == "=":
            self.advance()
            tok_type = TT_LTE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())

    def make_greater_than(self) -> Token:
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == "=":
            self.advance()
            tok_type = TT_GTE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())

    def skip_comment(self) -> None:
        self.advance()
        while self.current_char is not None and self.current_char != "\n":
            self.advance()
```

## File: `src\libs\channel.zyx`
```python
# libs.channel

namespace channel
    defun new()
        return channel_new_fp()
    done

    defun is_empty(ch)
        return channel_is_empty_fp(ch)
    done
    
    defun send(ch, value)
        channel_send_fp(ch, value)
        return none
    done

    defun recv(ch)
        return channel_receive_fp(ch)
    done
done
```

## File: `src\libs\csv.zyx`
```python
# libs.csv

namespace csv
    defun write(f, data)
        write_csv_fp(f, data)
        return none
    done

    defun read(f)
        return read_csv_fp(f)
    done
done
```

## File: `src\libs\decorators.zyx`
```python
# libs.decorators

namespace decorators
    load "libs.time"
    load "libs.threading"
    load "libs.json"

    defun name(fn) -> slice(to_str(fn), 10, -1)

    defun cache(fn)
        cache_map = {}
        defun wrapper(*args, **kwargs)
            using parent cache_map
            key = json.stringify([args, kwargs])
            if has(cache_map, key) do
                return cache_map$key
            done
            res = fn(*args, **kwargs)
            cache_map$key = res
            println(cache_map)
            return res
        done
        return wrapper
    done

    defun once(fn)
        has_run = false
        result = none

        defun wrapper(*vargs, **kargs)
            using parent has_run
            using parent result
            if has_run do
                return result
            done
            result = fn(*vargs, **kargs)
            has_run = true
            return result
        done
        return wrapper
    done

    defun retry(times)
        defun decorator(fn)
            defun wrapper(*vargs, **kargs)
                for i = 1 to times + 1 do
                    res = is_panic(fn, vargs)
                    result = res$0
                    err = res$1
                    
                    if is_none(err) do
                        return result
                    done
                    
                    println("Attempt " + to_str(i) + "/" + to_str(times) + " failed: " + err)
                done
                
                panic("Function '" + name(fn) + "' failed after " + to_str(times) + " retries", "RT")
            done
            return wrapper
        done
        return decorator
    done

    defun timeout(ms)
        defun decorator(fn)
            defun wrapper(*vargs, **kargs)
                state = {"result": none, "error": none, "done": false}

                defun target()
                    res = is_panic(fn, vargs)
                    if res$1 do
                        state$"error" = res$1
                    else do
                        state$"result" = res$0
                    done
                    state$"done" = true
                done

                t = threading.start(target)
                threading.join(t, timeout=(ms / 1000.0))

                if not state$"done" do
                    panic("Function '" + name(fn) + "' timed out after " + to_str(ms) + "ms", "RT")
                done
                
                if state$"error" do
                    panic(state$"error", "RT")
                done

                return state$"result"
            done
            return wrapper
        done
        return decorator
    done

    defun log_call(fn)
        defun wrapper(*vargs, **kargs)
            println("--> Calling function '" + name(fn) + "'...")
            result = fn(*vargs, **kargs)
            println("<-- Function '" + name(fn) + "' returned.")
            return result
        done
        return wrapper
    done
    
    defun measure_time(fn)
        defun wrapper(*vargs, **kargs)
            start = time.time()
            result = fn(*vargs, **kargs)
            end = time.time()
            duration = (end - start) * 1000
            println("Execution time for '" + name(fn) + "': " + to_str(duration) + " ms")
            return result
        done
        return wrapper
    done

    defun repeat(n)
        defun decorator(fn)
            defun wrapper(*vargs, **kargs)
                last_result = none
                for i = 1 to n + 1 do
                    last_result = fn(*vargs, **kargs)
                done
                return last_result
            done
            return wrapper
        done
        return decorator
    done

    defun ignore_error(default=none)
        defun decorator(fn)
            defun wrapper(*vargs, **kargs)
                res = is_panic(fn, vargs)
                if res$1 do
                    return default
                done
                return res$0
            done
            return wrapper
        done
        return decorator
    done

    defun deprecated(msg)
        defun decorator(fn)
            defun wrapper(*vargs, **kargs)
                println("DEPRECATION WARNING: Function '" + name(fn) + "' is deprecated. " + msg)
                return fn(*vargs, **kargs)
            done
            return wrapper
        done
        return decorator
    done
    
    defun lazy(fn)
        computed = false
        value = none
        
        defun wrapper(*vargs, **kargs)
            using parent computed
            using parent value
            if computed do
                return value
            done
            
            value = fn(*vargs, **kargs)
            computed = true
            return value
        done
        return wrapper
    done
done
```

## File: `src\libs\ffio.zyx`
```python
# libs.ffio (File Folder I/O)

namespace ffio
    os_sep = os_sep_fp

    defun write(f, m, t)
        if m != "w" and m != "a" and m != "wb" do
            panic("Invalid mode for write operation", "IO")
        done
        f_ = open_fp(f)
        write_fp(f_, m, t)
    done

    defun read(f, m)
        if m != "r" and m != "rb" do
            panic("Invalid mode for write operation", "IO")
        done
        if not exists_fp(f) do
            panic("File does not exist", "IO")
        done
        if type(f) != str do
            panic("First argument of 'read' must be a string", "T")
        done
        f_ = open_fp(f)
        return read_fp(f_, m)
    done

    defun exists(f)
        return exists_fp(f)
    done

    defun get_cdir()
        return get_cdir_fp()
    done

    defun set_cdir(n)
        set_cdir_fp(n)
        return none
    done

    defun list_dir(dir=".")
        return list_dir_fp(dir)
        return none
    done

    defun make_dir(d)
        mkdir_fp(d)
    done

    defun remove_file(f)
        remove_fp(f)
        return none
    done

    defun rename(o, n)
        rename_fp(o, n)
        return none
    done

    defun remove_dir(d)
        rmtree_fp(d)
        return none
    done

    defun copy(s, d)
        copy_fp(s, d)
        return none
    done

    defun is_file(f)
        return is_file_fp(f)
    done

    defun abs_path(p)
        return abs_path_fp(p)
    done

    defun base_name(p)
        return base_name_fp(p)
    done

    defun dir_name(p)
        return dir_name_fp(p)
    done

    defun symlink(s, d)
        symlink_fp(s, d)
        return none
    done

    defun readlink(p)
        return readlink_fp(p)
    done

    defun stat(p)
        return stat_fp(p)
    done

    defun lstat(p)
        return lstat_fp(p)
    done

    defun walk(t)
        return walk_fp(t)
    done

    defun chmod(p, m)
        chmod_fp(p, m)
        return none
    done

    defun chown(p, u, g)
        chown_fp(p, u, g)
        return none
    done

    defun utime(p, t)
        utime_fp(p, t)
        return none
    done

    defun link(s, d)
        link_fp(s, d)
        return none
    done

    defun unlink(p)
        unlink_fp(p)
        return none
    done

    defun access(p, m)
        return access_fp(p, m)
    done

    defun path_join(a)
        return path_join_fp(a)
    done

    defun is_dir(p)
        return is_dir_fp(p)
    done

    defun is_link(p)
        return is_link_fp(p)
    done

    defun is_mount(p)
        return is_mount_fp(p)
    done
done
```

## File: `src\libs\hash.zyx`
```python
# libs.hash

namespace hash
    defun md5(s)
        return md5_fp(s)
    done

    defun sha1(s)
        return sha1_fp(s)
    done

    defun sha256(s)
        return sha256_fp(s)
    done

    defun sha512(s)
        return sha512_fp(s)
    done

    defun crc32(s)
        return crc32_fp(s)
    done
done
```

## File: `src\libs\json.zyx`
```python
# libs.json

namespace json
    defun parse(s)
        return parse_fp(s)
    done

    defun stringify(o)
        return stringify_fp(o)
    done
done
```

## File: `src\libs\keyboard.zyx`
```python
# libs.keyboard

namespace keyboard
    defun write(t)
        keyboard_write_fp(t)
        return none
    done

    defun press(k)
        keyboard_press_fp(k)
        return none
    done

    defun release(k)
        keyboard_release_fp(k)
        return none
    done

    defun wait(k)
        keyboard_wait_fp(k)
        return none
    done

    defun is_pressed(k)
        return keyboard_is_pressed_fp(k)
    done
done
```

## File: `src\libs\listm.zyx`
```python
# libs.listm

namespace listm
    load "libs.random"

    defun map(f, l)
        if type(l) != list do
            panic("Second argument of 'map' must be a list", "T")
        done
        if type(f) != func do
            panic("First argument of 'map' must be a function", "T")
        done
        r = []
        for i = 0 to len(l) do
            append(r, f(l$i))
        done
        return r
    done

    defun rand_int_list(l, m, m_)
        l_ = []
        for _ = 0 to l do
            append(l_, random.rand_int(m, m_))
        done
        return l_
    done

    defun rand_float_list(l, m, m_)
        l_ = []
        for _ = 0 to l do
            append(l_, random.rand_float(m, m_))
        done
        return l_
    done

    defun filter(f, l)
        if type(l) != list do
            panic("Second argument of 'filter' must be a list", "T")
        done
        if type(f) != func do
            panic("First argument of 'filter' must be a function", "T")
        done
        r = []
        for i = 0 to len(l) do
            if f(l$i) do
                append(r, l$i)
            done
        done
        return r
    done

    defun reduce(f, l, i)
        if type(l) != list do
            panic("Second argument of 'reduce' must be a list", "T")
        done
        if type(f) != func do
            panic("First argument of 'reduce' must be a function", "T")
        done
        if type(i) != int and type(i) != float do
            panic("Third argument of 'reduce' must be a number", "T")
        done
        acc = i
        for i = 0 to len(l) do
            acc = f(acc, l$i)
        done
        return acc
    done

    defun min(l)
        if type(l) != list do
            panic("First argument of 'min' must be a list", "T")
        done
        if len(l) == 0 do
            panic("First argument of 'min' must be a list of numbers", "T")
        done
        m = l$0
        for i = 0 to len(l) do
            if type(l$i) != int and type(l$i) != float do
                panic("First argument of 'min' must be a list of numbers", "T")
            done
            if (l$i) < m do
                m = l$i
            done
        done
        return m
    done

    defun max(l)
        if type(l) != list do
            panic("First argument of 'max' must be a list", "T")
        done
        if len(l) == 0 do
            panic("First argument of 'max' must be a list of numbers", "T")
        done
        m = l$0
        for i = 0 to len(l) do
            if type(l$i) != int and type(l$i) != float do
                panic("First argument of 'max' must be a list of numbers", "T")
            done
            if (l$i) > m do
                m = l$i
            done
        done
        return m
    done

    defun reverse(l)
        r = []
        if type(l) != list do
            panic("First argument of 'reverse' must be a list", "T")
        done
        for i = len(l) - 1 to -1 step -1 do
            append(r, l$i)
        done
        return r
    done

    defun zip(l, l_)
        r = []
        if type(l) != list do
            panic("First argument of 'zip' must be a list", "T")
        elif type(l_) != list do
            panic("Second argument of 'zip' must be a list", "T")
        done
        _l = min([len(l), len(l_)])
        for i = 0 to _l do
            append(r, [l$i, l_$i])
        done
        return r
    done

    defun zip_longest(l, l_)
        r = []
        if type(l) != list do
            panic("First argument of 'zip_longest' must be a list", "T")
        done
        if type(l_) != list do
            panic("Second argument of 'zip_longest' must be a list", "T")
        done
        m = max([len(l), len(l_)])
        for i = 0 to m do
            v1 = none
            v2 = none
            if i < len(l) do
                v1 = l$i
            done
            if i < len(l_) do
                v2 = l_$i
            done
            append(r, [v1, v2])
        done
        return r
    done

    defun sort(l, reverse=false)
        if type(l) != list do
            panic("First argument of 'sort' must be a list", "T")
        done
        if not (len(filter(defun a(x) -> if type(x) == str do return true else do return false, l)) == len(l) or len(filter(defun a(x) -> if type(x) == int or type(x) == float do return true else do return false, l)) == len(l)) do
            panic("All elements of the list must be a either numbers or strings", "T")
        done
        s = sort_fp(l, reverse)
        return s
    done

    defun count(l, v)
        if type(l) != list do
            panic("First argument of 'count' must be a list", "T")
        done
        c = 0
        for i = 0 to len(l) do
            if type(l$i) != str and type(v) == str do
                if to_str(l$i) == v do
                    c = c + 1
                done
            else do
                if l$i == v do
                    c = c + 1
                done
            done
        done
        return c
    done

    defun index_of(l, v)
        if type(l) != list do
            panic("First argument of 'index_of' must be a list", "T")
        done
        for i = 0 to len(l) do
            if type(l$i) != str and type(v) == str do
                if to_str(l$i) == v do
                    return i
                done
            else do
                if l$i == v do
                    return i
                done
            done
        done
        return none
    done
done
```

## File: `src\libs\math.zyx`
```python
# libs.math

namespace math
    PI = PI_fp
    E = E_fp

    defun pass()
        none
    done

    defun check_number(a, b, f)
        if type(a) != int and type(a) != float and type(a) != cfloat do
            panic("First argument of '" + f + "' must be a number or cfloat", "T")
        done
        if b == none do
            pass()
        else do
            if type(b) != int and type(b) != float and type(b) != cfloat do
                panic("Second argument of '" + f + "' must be a number or cfloat", "T")
            done
        done
    done

    defun sqrt(a)
        check_number(a, none, "sqrt")
        if a < 0 do
            panic("Square root of negative number error", "M")
        done
        return sqrt_fp(a)
    done

    defun abs(a)
        check_number(a, none, "abs")
        return abs_fp(a)
    done

    defun fact(n)
        check_number(n, none, "fact")
        if n < 0 do
            panic("'fact' is undefined for negative number", "M")
        done
        return fact_fp(n)
    done

    defun sin(x)
        check_number(x, none, "sin")
        return sin_fp(x)
    done

    defun cos(x)
        check_number(x, none, "cos")
        return cos_fp(x)
    done

    defun tan(x)
        check_number(x, none, "tan")
        k = to_int(x / (PI / 2), false)
        if (k % 2 != 0) and (abs(x - (k * PI / 2)) < (1 * 10^ (-15))) do
            panic("'tan' is undefined at this value", "M")
        done
        return tan_fp(x)
    done

    defun gcd(a, b)
        check_number(a, b, "gcd")
        return gcd_fp(a, b)
    done

    defun lcm(a, b)
        check_number(a, b, "lcm")
        return lcm_fp(a, b)
    done

    defun fib(n)
        check_number(n, none, "fib")
        if n < 0 do
            panic("'fib' is undefined for negative number", "M")
        done
        return fib_fp(n)
    done

    defun is_prime(n)
        check_number(n, none, "is_prime")
        return is_prime_fp(n)
    done

    defun deg2rad(d)
        check_number(d, none, "deg2rad")
        return deg2rad_fp(d)
    done

    defun rad2deg(r)
        check_number(r, none, "rad2deg")
        return rad2deg_fp(r)
    done

    defun exp(x)
        check_number(x, none, "exp")
        return exp_fp(x)
    done

    defun log(x)
        check_number(x, none, "log")
        if x <= 0 do
            panic("'log' is undefined at this value", "M")
        done
        return log_fp(x)
    done

    ln2 = log(2)

    defun sinh(x)
        check_number(x, none, "sinh")
        return sinh_fp(x)
    done

    defun cosh(x)
        check_number(x, none, "cosh")
        return cosh_fp(x)
    done

    defun tanh(x)
        check_number(x, none, "tanh")
        return tanh_fp(x)
    done

    defun round(x)
        check_number(x, none, "round")
        return round_fp(x)
    done

    defun is_close(v1, v2, rel_tol=1*10^(-9), abs_tol=0.0)
        check_number(v1, v2, "is_close")
        if type(rel_tol) != int and type(rel_tol) != float do
            panic("Third argument of 'is_close' must be a number", "T")
        done
        if type(abs_tol) != int and type(abs_tol) != float do
            panic("Fourth argument of 'is_close' must be a number", "T")
        done
        return is_close_fp(v1, v2, rel_tol, abs_tol)
    done
done
```

## File: `src\libs\memory.zyx`
```python
# libs.memory

memory_private_mem_36 = {}

namespace memory
    defun remember(k, v)
        memory_private_mem_36$k = v
    done

    defun recall(k)
        return get(memory_private_mem_36, k)
    done

    defun forget(k)
        del_key(memory_private_mem_36, k)
    done

    defun clear_memory()
        using memory_private_mem_36
        memory_private_mem_36 = {}
    done

    defun keys()
        return keys(memory_private_mem_36)
    done

    defun is_empty()
        return len(memory_private_mem_36) == 0
    done

    defun size()
        return len(memory_private_mem_36)
    done
done
```

## File: `src\libs\mouse.zyx`
```python
# libs.mouse

namespace mouse
    defun move(x, y)
        mouse_move_fp(x, y)
        return none
    done

    defun click()
        mouse_click_fp()
        return none
    done

    defun right_click()
        right_click_fp()
        return none
    done

    defun scroll(amount)
        mouse_scroll_fp(amount)
        return none
    done

    defun position()
        return mouse_position_fp()
    done
done
```

## File: `src\libs\msgbox.zyx`
```python
# libs.msgbox

namespace msgbox
    defun alert(message, title)
        return msgbox_alert_fp(message, title)
    done

    defun confirm(message, title, buttons=["OK", "Cancel"])
        return msgbox_confirm_fp(message, title, buttons)
    done

    defun prompt(message, title)
        return msgbox_prompt_fp(message, title)
    done

    defun password(message, title)
        return msgbox_password_fp(message, title)
    done
done
```

## File: `src\libs\net.zyx`
```python
# libs.net

namespace net
    defun get_ip()
        return get_ip_fp()
    done

    defun get_mac()
        return get_mac_fp()
    done

    defun ping(h)
        return ping_fp(h)
    done

    defun download(u, timeout=15)
        return downl_fp(u, timeout)
    done

    defun get_local_ip()
        return get_local_ip_fp()
    done

    defun get_hostname()
        return get_hostname_fp()
    done

    defun request(url, method="GET", headers={}, data={}, timeout=15)
        return request_fp(url, method, headers, data, timeout)
    done
done
```

## File: `src\libs\random.zyx`
```python
# libs.random

namespace random
    defun rand()
        return rand_fp()
    done

    defun rand_int(m, m_)
        return rand_int_fp(m, m_)
    done

    defun rand_float(m, m_)
        return rand_float_fp(m, m_)
    done

    defun rand_choice(l)
        if type(l) != list do
            panic("First argument of 'rand_choice' must be a list", "T")
        done
        if len(l) == 0 do
            panic("Can't choose from an empty list", "T")
        done
        return rand_choice_fp(l)
    done

    defun int_seed(i)
        if type(i) != int and type(i) != float do
            panic("First argument of 'int_seed' must be a number", "T")
        done
        return (i * 1664525 + 1013904223) % (2^32)
    done

    defun float_seed(f)
        if type(i) != int and type(i) != float do
            panic("First argument of 'float_seed' must be a number", "T")
        done
        return int_seed(f / (2^32))
    done
done
```

## File: `src\libs\screen.zyx`
```python
# libs.screen

namespace screen
    defun capture(p)
        screen_capture_fp(p)
        return none
    done

    defun capture_area(x, y, w, h, p)
        screen_capture_area_fp(x, y, w, h, p)
        return none
    done

    defun get_color(x, y)
        return screen_get_color(x, y)
    done
done
```

## File: `src\libs\string.zyx`
```python
# libs.string

namespace string
    digits = "0123456789"
    ascii_lowercase = "abcdefghijklmnopqrstuvwxyz"
    ascii_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ascii_letters = ascii_lowercase + ascii_uppercase
    list_digits = split_fp(digits, "")
    list_ascii_lowercase = split_fp(ascii_lowercase, "")
    list_ascii_uppercase = split_fp(ascii_uppercase, "")
    list_ascii_letters = split_fp(ascii_letters, "")

    defun split(s, sep="")
        return split_fp(s, sep)
    done

    defun strip(s, sep=" ")
        return strip_fp(s, sep)
    done 

    defun join(s, l)
        return join_fp(s, l)
    done

    defun replace(s, v, w, c=-1)
        return replace_fp(s, v, w, c)
    done

    defun to_upper(s)
        return to_upper_fp(s)
    done

    defun to_lower(s)
        return to_lower_fp(s)
    done

    defun ord(s)
        return to_str(ord_fp(s))
    done

    defun chr(n)
        return to_str(chr_fp(n))
    done

    defun is_digit(s)
        if not is_str(s) do
            return false
        done
        if len(s) != 1 do
            return false
        done
        for i = 0 to len(list_digits) do
            if s == list_digits$i do
                return true
            done
        done
        return false
    done

    defun is_ascii_lowercase(s)
        if not is_str(s) do
            return false
        done
        if len(s) != 1 do
            return false
        done
        for i = 0 to len(list_ascii_lowercase) do
            if s == list_ascii_lowercase$i do
                return true
            done
        done
        return false
    done

    defun is_ascii_uppercase(s)
        if not is_str(s) do
            return false
        done
        if len(s) != 1 do
            return false
        done
        for i = 0 to len(list_ascii_uppercase) do
            if s == list_ascii_uppercase$i do
                return true
            done
        done
        return false
    done

    defun is_ascii_letter(s)
        if not is_str(s) do
            return false
        done
        if len(s) != 1 do
            return false
        done
        for i = 0 to len(list_ascii_letters) do
            if s == list_ascii_letters$i do
                return true
            done
        done
        return false
    done

    defun is_space(s)
        if not is_str(s) do
            return false
        done
        if len(s) != 1 do
            return false
        done
        return (s == " " or s == "\t" or s == "\n" or s == "\r" or s == "\v" or s == "\f")
    done

    defun find(s, v)
        return find_fp(s, v)
    done

    defun find_all(s, v)
        result = []
        start = 0
        while true do
            sub = slice(s, start, none, none)
            idx = find(sub, v)
            if is_none(idx) do
                break
            done
            append(result, start + idx)
            start = start + idx + 1
        done
        return result
    done

    defun startswith(s, v)
        if not is_str(s) do
            panic("First argument of 'startswith' must be a string", "T")
        done
        if not is_str(v) do
            panic("Second argument of 'startswith' must be a string", "T") 
        done
        if len(v) == 0 or len(s) == 0 do
            return false
        done
        if len(v) > len(s) do
            return false
        done
        prefix = slice(s, 0, len(v), none)
        return prefix == v
    done

    defun endswith(s, v)
        if not is_str(s) do
            panic("First argument of 'endswith' must be a string", "T")
        done
        if not is_str(v) do
            panic("Second argument of 'endswith' must be a string", "T")
        done
        if len(v) == 0 or len(s) == 0 do
            return false
        done
        if len(v) > len(s) do
            return false
        done
        suffix = slice(s, len(s) - len(v), none, none) 
        return suffix == v
    done

    defun encode(s, e, e_)
        return encode_fp(s, e, e_)
    done

    defun decode(s, e, e_)
        return decode_fp(s, e, e_)
    done

    defun format(s, l)
        return string_format_fp(s, l)
    done
done
```

## File: `src\libs\sys.zyx`
```python
# libs.sys

namespace sys
    argv = argv_fp
    os_name = os_name_fp

    defun system(c)
        system_fp(c)
        return none
    done

    defun osystem(c)
        return osystem_fp(c)
    done

    defun get_env(n)
        return get_env_fp(n)
        return none
    done

    defun set_env(n, v)
        set_env_fp(n, v)
        return none
    done

    defun exit(exit_code=0)
        exit_fp(exit_code)
    done
done
```

## File: `src\libs\termcolor.zyx`
```python
# libs.termcolor

namespace termcolor
    load "libs.string"

    color_map = [
        ['black', 30], ['red', 31], ['green', 32], ['yellow', 33],
        ['blue', 34], ['magenta', 35], ['cyan', 36], ['white', 37]
    ]
    bg_map = [
        ['on_black', 40], ['on_red', 41], ['on_green', 42], ['on_yellow', 43],
        ['on_blue', 44], ['on_magenta', 45], ['on_cyan', 46], ['on_white', 47]
    ]
    style_map = [
        ['bold', 1], ['underline', 4], ['reverse', 7]
    ]

    defun get_color(name)
        for i = 0 to len(color_map) do
            color = color_map$i
            if color$0 == name do
                return to_str(color$1)
            done
        done
        return ''
    done

    defun get_bg(name)
        for i = 0 to len(bg_map) do
            bg = bg_map$i
            if bg$0 == name do
                return to_str(bg$1)
            done
        done
        return ''
    done

    defun get_style(name)
        for i = 0 to len(style_map) do
            style = style_map$i
            if style$0 == name do
                return to_str(style$1)
            done
        done
        return ''
    done

    defun get_code(color=none, background=none, style=none)
        color_code = ''
        bg_code = ''
        style_code = ''
        if not is_none(color) do
            color_code = get_color(color)
        done
        if not is_none(background) do
            bg_code = get_bg(background)
        done
        if not is_none(style) do
            style_code = get_style(style)
        done
        all_codes = []
        if color_code != '' do
            all_codes = all_codes + color_code
        done
        if bg_code != '' do
            all_codes = all_codes + bg_code
        done
        if style_code != '' do
            all_codes = all_codes + style_code
        done
        return string.join(';', all_codes)
    done

    defun cprint(t, color=none, background=none, style=none)
        code_str = get_code(color, background, style)
        if not is_none(code_str) do
            print(string.chr(27) + '[' + code_str + 'm' + to_str(t) + string.chr(27) + '[0m')
        else do
            print(t)
        done
        return none
    done

    defun cprintln(t, color=none, background=none, style=none)
        code_str = get_code(color, background, style)
        if not is_none(code_str) do
            println(string.chr(27) + '[' + code_str + 'm' + to_str(t) + string.chr(27) + '[0m')
        else do
            println(t)
        done
        return none
    done
done
```

## File: `src\libs\threading.zyx`
```python
# libs.threading

namespace threading
    defun start(f, args=[], kwargs={})
        return thread_start_fp(f, args, kwargs)
    done

    defun sleep(s)
        thread_sleep_fp(s)
    done

    defun join(h, timeout=15)
        thread_join_fp(h, timeout)
    done

    defun is_alive(t)
        return thread_is_alive_fp(t)
    done

    defun cancel(t)
        thread_cancel_fp(t)
    done
    
    namespace pool
        defun new(max_workers=5)
            return thread_pool_new_fp(max_workers)
        done

        defun submit(pool, func, args=[], kwargs={})
            return thread_pool_submit_fp(pool, func, args, kwargs)
        done

        defun shutdown(pool, wait=true)
            thread_pool_shutdown_fp(pool, wait)
        done

        defun result(future)
            return future_result_fp(future)
        done

        defun is_done(future)
            return future_done_fp(future)
        done
    done
done
```

## File: `src\libs\time.zyx`
```python
# libs.time

namespace time
    defun sleep(s)
        sleep_fp(s)
        return none
    done

    defun time()
        return time_fp()
    done

    defun ctime(t)
        return ctime_fp(t)
    done

    namespace datetime
        defun now()
            return datetime_now_fp()
        done

        defun today()
            return date_today_fp()
        done

        defun format(fmt)
            return datetime_format_fp(fmt)
        done

        defun parse(s, fmt)
            return datetime_parse_fp(s, fmt)
        done

        defun add_days(days)
            return datetime_add_days_fp(days)
        done

        defun diff(dt1, dt2)
            return datetime_diff_fp(dt1, dt2)
        done
    done
done
```

## File: `src\nodes.py`
```python
class NumberNode:
    __slots__ = ["tok", "pos_start", "pos_end"]

    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"

    def __str__(self):
        return f"NumberNode({self.tok.value})"


class StringNode:
    __slots__ = ["tok", "pos_start", "pos_end"]

    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"

    def __str__(self):
        return f'StringNode("{self.tok.value}")'


class ListNode:

    __slots__ = ["element_nodes", "pos_start", "pos_end"]

    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __str__(self):
        return f"ListNode({', '.join(str(x) for x in self.element_nodes)})"


class VarAccessNode:
    __slots__ = ["var_name_tok", "pos_start", "pos_end"]

    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __str__(self):
        return f"VarAccessNode({self.var_name_tok.value})"


class VarAssignNode:
    __slots__ = ["var_name_tok", "value_node", "pos_start", "pos_end"]

    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

    def __str__(self):
        return f"VarAssignNode({self.var_name_tok.value} = {self.value_node})"


class BinOpNode:
    __slots__ = ["left_node", "op_tok", "right_node", "pos_start", "pos_end"]

    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"

    def __str__(self):
        return f"BinOpNode({self.left_node} {self.op_tok.type} {self.right_node})"


class UnaryOpNode:
    __slots__ = ["op_tok", "node", "pos_start", "pos_end"]

    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"

    def __str__(self):
        return f"UnaryOpNode({self.op_tok.type}{self.node})"


class IfNode:
    __slots__ = ["cases", "else_case", "pos_start", "pos_end"]

    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end

    def __str__(self):
        result = "IfNode("
        for condition, expr, _ in self.cases:
            result += f"\nif {condition} do {expr}"
        if self.else_case:
            expr, _ = self.else_case
            result += f"\nelse {expr}"
        return result + ")"


class ForNode:
    __slots__ = [
        "var_name_tok",
        "start_value_node",
        "end_value_node",
        "step_value_node",
        "body_node",
        "should_return_none",
        "pos_start",
        "pos_end",
    ]

    def __init__(
        self,
        var_name_tok,
        start_value_node,
        end_value_node,
        step_value_node,
        body_node,
        should_return_none,
    ):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.should_return_none = should_return_none
        self.pos_start = self.var_name_tok.pos_start

        if body_node:
            self.pos_end = self.body_node.pos_end
        elif step_value_node:
            self.pos_end = self.step_value_node.pos_end
        else:
            self.pos_end = self.end_value_node.pos_end

    def __str__(self):
        return f"ForNode({self.var_name_tok.value} from {self.start_value_node} to {self.end_value_node} step {self.step_value_node} do {self.body_node})"


class WhileNode:
    __slots__ = [
        "condition_node",
        "body_node",
        "should_return_none",
        "pos_start",
        "pos_end",
    ]

    def __init__(self, condition_node, body_node, should_return_none):
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_none = should_return_none
        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __str__(self):
        return f"WhileNode(while {self.condition_node} do {self.body_node})"


class FuncDefNode:
    def __init__(
        self,
        var_name_tok,
        arg_name_toks,
        defaults,
        vargs_name_tok,
        kargs_name_tok,
        body_node,
        should_auto_return,
        decorator_nodes,
    ):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.defaults = defaults
        self.vargs_name_tok = vargs_name_tok
        self.kargs_name_tok = kargs_name_tok
        self.body_node = body_node
        self.should_auto_return = should_auto_return
        self.decorator_nodes = decorator_nodes

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start
        self.pos_end = self.body_node.pos_end


class VargsUnpackNode:
    __slots__ = ["node_to_unpack", "pos_start", "pos_end"]

    def __init__(self, node_to_unpack):
        self.node_to_unpack = node_to_unpack
        self.pos_start = node_to_unpack.pos_start
        self.pos_end = node_to_unpack.pos_end


class KargsUnpackNode:
    __slots__ = ["node_to_unpack", "pos_start", "pos_end"]

    def __init__(self, node_to_unpack):
        self.node_to_unpack = node_to_unpack
        self.pos_start = node_to_unpack.pos_start
        self.pos_end = node_to_unpack.pos_end


class CallNode:
    def __init__(self, node_to_call, arg_nodes, pos_start=None, pos_end=None):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes
        self.pos_start = pos_start or node_to_call.pos_start
        self.pos_end = pos_end or (
            arg_nodes[-1].pos_end if arg_nodes else node_to_call.pos_end
        )

    def __repr__(self):
        return f"(Call: {self.node_to_call} with {self.arg_nodes})"


class ReturnNode:
    __slots__ = ["node_to_return", "pos_start", "pos_end"]

    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __str__(self):
        return f"ReturnNode({self.node_to_return})"


class ContinueNode:
    __slots__ = ["pos_start", "pos_end"]

    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __str__(self):
        return "ContinueNode()"


class BreakNode:
    __slots__ = ["pos_start", "pos_end"]

    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __str__(self):
        return "BreakNode()"


class AccessNode:

    def __init__(self, obj, index):
        self.obj = obj
        self.index = index

    def __str__(self):
        return f"AccessNode({self.obj}[{self.index}])"


class LoadNode:
    __slots__ = ["module_name_tok", "file_path", "pos_start", "pos_end"]

    def __init__(self, module_name_tok):
        self.module_name_tok = module_name_tok
        self.file_path = module_name_tok.value
        self.pos_start = self.module_name_tok.pos_start
        self.pos_end = self.module_name_tok.pos_end

    def __str__(self):
        return f'LoadNode("{self.file_path}")'


class HashMapNode:
    __slots__ = ["pairs", "pos_start", "pos_end"]

    def __init__(self, pairs, pos_start, pos_end):
        self.pairs = pairs
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __str__(self):
        return f"HashMapNode({', '.join(f'{k}: {v}' for k, v in self.pairs)})"


class ForInNode:
    __slots__ = [
        "var_name_toks",
        "iterable_node",
        "body_node",
        "pos_start",
        "pos_end",
        "should_return_none",
    ]

    def __init__(
        self,
        var_name_toks,
        iterable_node,
        body_node,
        should_return_none,
        pos_start=None,
        pos_end=None,
    ):
        self.var_name_toks = var_name_toks
        self.iterable_node = iterable_node
        self.body_node = body_node
        self.should_return_none = should_return_none
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __str__(self):
        var_names = ", ".join(tok.value for tok in self.var_name_toks)
        return f"ForInNode({var_names} in {self.iterable_node} do {self.body_node})"


class NameSpaceNode:
    __slots__ = ["namespace_name", "statements", "pos_start", "pos_end"]

    def __init__(self, namespace_name, statements, pos_start, pos_end):
        self.namespace_name = (
            namespace_name if isinstance(namespace_name, str) else namespace_name.value
        )
        self.statements = statements
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"NameSpaceNode({self.namespace_name}, {self.statements})"


class MemberAccessNode:
    __slots__ = ["object_node", "member_name", "pos_start", "pos_end"]

    def __init__(self, object_node, member_name, pos_start, pos_end):
        self.object_node = object_node
        self.member_name = member_name
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"(MemberAccessNode {self.object_node}.{self.member_name})"


class NamedArgumentNode:
    def __init__(self, param_name_tok, value_node, pos_start=None, pos_end=None):
        self.param_name_tok = param_name_tok
        self.value_node = value_node
        self.pos_start = pos_start or param_name_tok.pos_start
        self.pos_end = pos_end or value_node.pos_end

    def __repr__(self):
        return f"(NamedArg: {self.param_name_tok.value} = {self.value_node})"


class UsingNode:
    def __init__(self, var_name_toks, pos_start, pos_end):
        self.var_name_toks = var_name_toks
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"UsingNode({self.var_name_toks})"


class UsingParentNode:
    def __init__(self, var_name_toks, pos_start, pos_end):
        self.var_name_toks = var_name_toks
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"UsingParentNode({self.var_name_toks})"


class DelNode:
    def __init__(self, var_name_toks, pos_start, pos_end):
        self.var_name_toks = var_name_toks
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"DelNode({self.var_name_toks})"


class IndexAssignNode:
    def __init__(self, obj_node, index_node, value_node):
        self.obj_node = obj_node
        self.index_node = index_node
        self.value_node = value_node

        self.pos_start = self.obj_node.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self):
        return (
            f"IndexAssignNode({self.obj_node} [{self.index_node}] = {self.value_node})"
        )
```

## File: `src\parser.py`
```python
import os

from .consts import *
from .errors import InvalidSyntaxError
from .nodes import *
from .utils import Token


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self


class Parser:
    __slots__ = ("tokens", "tok_idx", "current_tok")

    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok = None
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok: Token = self.tokens[self.tok_idx]
        else:
            self.current_tok = None

    def skip_newlines(self) -> ParseResult:
        res = ParseResult()
        while self.current_tok and self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
        return res

    def parse(self):
        self.skip_newlines()
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    f"Unexpected token '{self.current_tok.type}'",
                )
            )
        return res

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        self.skip_newlines()

        res.register(self.skip_newlines())

        statement = res.register(self.statement())
        if res.error:
            return res
        statements.append(statement)

        more_statements = True
        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1

            if newline_count == 0:
                more_statements = False

            if not more_statements:
                break

            self.skip_newlines()
            statement = res.try_register(self.statement())

            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue

            statements.append(statement)

        return res.success(
            ListNode(statements, pos_start, self.current_tok.pos_end.copy())
        )

    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type == TT_AND:
            decorator_nodes = []
            while self.current_tok.type == TT_AND:
                res.register_advancement()
                self.advance()
                decorator_nodes.append(res.register(self.expr(allow_assignment=False)))
                if res.error:
                    return res
                self.skip_newlines()

            if not self.current_tok.matches(TT_KEYWORD, "defun"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'defun' after decorator(s)",
                    )
                )

            func_def_node = res.register(self.func_def())
            if res.error:
                return res

            func_def_node.decorator_nodes = decorator_nodes
            return res.success(func_def_node)

        if self.current_tok.matches(TT_KEYWORD, "using"):
            return self.using_expr()

        if self.current_tok.matches(TT_KEYWORD, "del"):
            return self.del_expr()

        if self.current_tok.matches(TT_KEYWORD, "defun"):
            return self.func_def()

        if self.current_tok.matches(TT_KEYWORD, "return"):
            res.register_advancement()
            self.advance()

            expr = None
            if self.current_tok.type not in (
                TT_NEWLINE,
                TT_EOF,
            ) and not self.current_tok.matches(TT_KEYWORD, "done"):
                expr = res.try_register(self.expr(allow_assignment=False))
                if res.error:
                    return res

            return res.success(
                ReturnNode(expr, pos_start, self.current_tok.pos_start.copy())
            )

        if self.current_tok.matches(TT_KEYWORD, "continue"):
            res.register_advancement()
            self.advance()
            return res.success(
                ContinueNode(pos_start, self.current_tok.pos_start.copy())
            )

        if self.current_tok.matches(TT_KEYWORD, "break"):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'return', 'continue', 'break', 'if', 'for', 'while', 'defun', int, float, identifier, '+', '-', '(', '[', '{' or 'not'",
                )
            )
        return res.success(expr)

    def peek_tok(self) -> Token:
        if self.tok_idx + 1 >= len(self.tokens):
            return None
        return self.tokens[self.tok_idx + 1]

    def peek_tok_back(self) -> Token:
        if self.tok_idx - 1 < 0:
            return None
        return self.tokens[self.tok_idx - 1]

    def expr(self, allow_assignment=True):
        res = ParseResult()

        node = res.register(self.assignment_expr(allow_assignment))

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'if', 'for', 'while', 'defun', int, float, identifier, '+', '-', '(', '[', '{' or 'not'",
                )
            )

        return res.success(node)

    def assignment_expr(self, allow_assignment=True):
        res = ParseResult()

        if allow_assignment:
            if self.current_tok.type == TT_IDENTIFIER:
                var_name_tok = self.current_tok
                res.register_advancement()
                self.advance()

                aug_ops = {
                    TT_PLUSEQ: TT_PLUS,
                    TT_MINUSEQ: TT_MINUS,
                    TT_MULEQ: TT_MUL,
                    TT_DIVEQ: TT_DIV,
                    TT_FLOORDIVEQ: TT_FLOORDIV,
                    TT_MODEQ: TT_MOD,
                    TT_POWEQ: TT_POW,
                }

                if self.current_tok.type == TT_EQ:
                    res.register_advancement()
                    self.advance()
                    value_node = res.register(self.expr())
                    if res.error:
                        return res
                    return res.success(VarAssignNode(var_name_tok, value_node))

                elif self.current_tok.type in aug_ops:
                    op_type = aug_ops[self.current_tok.type]
                    op_tok = Token(
                        op_type,
                        pos_start=self.current_tok.pos_start.copy(),
                        pos_end=self.current_tok.pos_end.copy(),
                    )
                    res.register_advancement()
                    self.advance()

                    value_node = res.register(self.expr())
                    if res.error:
                        return res

                    left_node = VarAccessNode(var_name_tok)
                    bin_op = BinOpNode(left_node, op_tok, value_node)
                    return res.success(VarAssignNode(var_name_tok, bin_op))

                self.reverse(res.advance_count)

        if self.current_tok.matches(TT_KEYWORD, "load"):
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_STRING:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected string",
                    )
                )
            module = self.current_tok
            raw_path = module.value.replace(".", os.sep)
            if raw_path.endswith(("\\", "/")):
                raw_path = raw_path[:-1]
            raw_path += ".zyx"
            candidates = []
            if module.value.startswith("libs."):
                candidates.append(raw_path)
            elif module.value.startswith("local."):
                if self.current_tok.pos_start.fn == "<stdin>":
                    local_path = os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), raw_path[6:]
                    )
                else:
                    local_path = os.path.join(
                        os.path.dirname(os.path.abspath(self.current_tok.pos_start.fn)),
                        raw_path[6:],
                    )
                candidates.append(local_path)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Paths must start with 'libs.' or 'local.'",
                    )
                )
            chosen_path = None
            for path in candidates:
                if os.path.exists(path):
                    chosen_path = path
                    break
            module.value = os.path.normpath(chosen_path or candidates[0])
            res.register_advancement()
            self.advance()
            return res.success(LoadNode(module))

        node = res.register(
            self.bin_op(self.comp_expr, ((TT_KEYWORD, "and"), (TT_KEYWORD, "or")))
        )

        if res.error:
            return res

        if isinstance(node, BinOpNode) and node.op_tok.type == TT_DOLLAR:

            aug_ops = {
                TT_PLUSEQ: TT_PLUS,
                TT_MINUSEQ: TT_MINUS,
                TT_MULEQ: TT_MUL,
                TT_DIVEQ: TT_DIV,
                TT_FLOORDIVEQ: TT_FLOORDIV,
                TT_MODEQ: TT_MOD,
                TT_POWEQ: TT_POW,
            }

            if self.current_tok.type == TT_EQ:
                res.register_advancement()
                self.advance()

                value_node = res.register(self.expr())
                if res.error:
                    return res

                return res.success(
                    IndexAssignNode(node.left_node, node.right_node, value_node)
                )

            elif self.current_tok.type in aug_ops:
                op_type = aug_ops[self.current_tok.type]
                op_tok = Token(
                    op_type,
                    pos_start=self.current_tok.pos_start.copy(),
                    pos_end=self.current_tok.pos_end.copy(),
                )
                res.register_advancement()
                self.advance()

                value_node = res.register(self.expr())
                if res.error:
                    return res

                bin_op = BinOpNode(node, op_tok, value_node)
                return res.success(
                    IndexAssignNode(node.left_node, node.right_node, bin_op)
                )

        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, "not"):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(
            self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE))
        )

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected int, float, identifier, '+', '-', '(', '[', '{', 'if', 'for', 'while', 'defun' or 'not'",
                )
            )

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_FLOORDIV, TT_MOD))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type == TT_MUL:
            res.register_advancement()
            self.advance()
            node_to_unpack = res.register(self.factor())
            if res.error:
                return res
            return res.success(VargsUnpackNode(node_to_unpack))

        elif tok.type == TT_DOUBLE_STAR:
            res.register_advancement()
            self.advance()
            node_to_unpack = res.register(self.factor())
            if res.error:
                return res
            return res.success(KargsUnpackNode(node_to_unpack))

        return self.dollar_op()

    def power(self):
        return self.bin_op(self.call, (TT_POW,))

    def dot_op(self):
        return self.bin_op(self.power, (TT_DOT,))

    def dollar_op(self):
        return self.bin_op(self.dot_op, (TT_DOLLAR,))

    def call(self):
        res = ParseResult()
        node = res.register(self.atom())
        if res.error:
            return res

        while self.current_tok.type == TT_DOT:
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected identifier",
                    )
                )

            member_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            node = MemberAccessNode(
                node,
                member_name_tok.value,
                node.pos_start,
                self.current_tok.pos_end.copy(),
            )

        if self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                while True:
                    self.skip_newlines()
                    if (
                        self.current_tok.type == TT_IDENTIFIER
                        and self.peek_tok()
                        and self.peek_tok().type == TT_EQ
                    ):
                        var_name_tok = self.current_tok
                        res.register_advancement()
                        self.advance()

                        res.register_advancement()
                        self.advance()

                        value_node = res.register(self.expr(allow_assignment=False))
                        if res.error:
                            return res
                        arg_nodes.append(VarAssignNode(var_name_tok, value_node))
                    else:
                        arg_nodes.append(
                            res.register(self.expr(allow_assignment=False))
                        )
                        if res.error:
                            return res.failure(
                                InvalidSyntaxError(
                                    self.current_tok.pos_start,
                                    self.current_tok.pos_end,
                                    "Expected ')', 'if', 'for', 'while', 'defun', int, float, identifier, '+', '-', '(', '[', '{' or 'not'",
                                )
                            )
                    self.skip_newlines()
                    if self.current_tok.type == TT_RPAREN:
                        res.register_advancement()
                        self.advance()
                        break
                    elif self.current_tok.type == TT_COMMA:
                        res.register_advancement()
                        self.advance()
                    else:
                        return res.failure(
                            InvalidSyntaxError(
                                self.current_tok.pos_start,
                                self.current_tok.pos_end,
                                "Expected ',' or ')'",
                            )
                        )
            return res.success(CallNode(node, arg_nodes))

        return res.success(node)

    def using_expr(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        res.register_advancement()
        self.advance()

        if self.current_tok.matches(TT_IDENTIFIER, "parent"):
            res.register_advancement()
            self.advance()

            node_class = UsingParentNode
            err_msg = "Expected identifier after 'using parent'"
        else:
            node_class = UsingNode
            err_msg = "Expected identifier after 'using'"

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, err_msg
                )
            )

        var_name_toks = [self.current_tok]
        res.register_advancement()
        self.advance()

        while self.current_tok.type == TT_COMMA:
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected identifier",
                    )
                )
            var_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

        return res.success(
            node_class(var_name_toks, pos_start, self.current_tok.pos_end.copy())
        )

    def del_expr(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected identifier after 'del'",
                )
            )

        var_name_toks = [self.current_tok]
        res.register_advancement()
        self.advance()

        while self.current_tok.type == TT_COMMA:
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected identifier",
                    )
                )
            var_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

        return res.success(
            DelNode(var_name_toks, pos_start, self.current_tok.pos_end.copy())
        )

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        elif tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))
        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))
        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr(allow_assignment=False))
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ')'",
                    )
                )
        elif tok.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error:
                return res
            return res.success(list_expr)
        elif tok.matches(TT_KEYWORD, "if"):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)
        elif tok.matches(TT_KEYWORD, "for"):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)
        elif tok.matches(TT_KEYWORD, "while"):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)
        elif tok.matches(TT_KEYWORD, "defun"):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)
        elif tok.matches(TT_KEYWORD, "namespace"):
            namespace = res.register(self.namespace())
            if res.error:
                return res
            return res.success(namespace)
        elif tok.type == TT_LBRACE:
            hashmap_expr = res.register(self.hashmap_expr())
            if res.error:
                return res
            return res.success(hashmap_expr)

        return res.failure(
            InvalidSyntaxError(
                tok.pos_start,
                tok.pos_end,
                "Expected int, float, identifier, '+', '-', '(', '[', '{', 'if', 'for', 'while', 'defun' or 'namespace'",
            )
        )

    def namespace(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if not self.current_tok.matches(TT_KEYWORD, "namespace"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'namespace'",
                )
            )
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected identifier",
                )
            )
        namespace_name = self.current_tok.value
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_NEWLINE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected newline",
                )
            )
        res.register_advancement()
        self.advance()

        statements = []
        while not self.current_tok.matches(TT_KEYWORD, "done"):
            self.skip_newlines()
            stmt = res.register(self.statement())
            if res.error:
                return res
            statements.append(stmt)
            self.skip_newlines()

        statements_node = ListNode(
            statements, pos_start, self.current_tok.pos_start.copy()
        )

        if not self.current_tok.matches(TT_KEYWORD, "done"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'done'",
                )
            )
        res.register_advancement()
        self.advance()

        return res.success(
            NameSpaceNode(
                namespace_name,
                statements_node,
                pos_start,
                self.current_tok.pos_end.copy(),
            )
        )

    def hashmap_expr(self) -> ParseResult:
        res = ParseResult()
        pairs = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LBRACE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"
                )
            )

        res.register_advancement()
        self.advance()
        self.skip_newlines()

        if self.current_tok.type == TT_RBRACE:
            res.register_advancement()
            self.advance()
            return res.success(
                HashMapNode([], pos_start, self.current_tok.pos_end.copy())
            )

        key = res.register(self.expr(allow_assignment=False))
        if res.error:
            return res

        if self.current_tok.type != TT_COLON:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, "Expected ':'"
                )
            )
        res.register_advancement()
        self.advance()

        value = res.register(self.expr(allow_assignment=False))
        if res.error:
            return res
        pairs.append((key, value))

        while self.current_tok.type == TT_COMMA:
            res.register_advancement()
            self.advance()
            self.skip_newlines()

            key = res.register(self.expr(allow_assignment=False))
            if res.error:
                return res
            self.skip_newlines()

            if self.current_tok.type != TT_COLON:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ':'",
                    )
                )
            res.register_advancement()
            self.advance()
            self.skip_newlines()

            value = res.register(self.expr(allow_assignment=False))
            if res.error:
                return res
            self.skip_newlines()
            pairs.append((key, value))

        self.skip_newlines()
        if self.current_tok.type != TT_RBRACE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected ',' or '}'",
                )
            )
        res.register_advancement()
        self.advance()

        return res.success(
            HashMapNode(pairs, pos_start, self.current_tok.pos_end.copy())
        )

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, "Expected '['"
                )
            )
        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
            return res.success(
                ListNode(element_nodes, pos_start, self.current_tok.pos_end.copy())
            )

        first_element = res.register(self.expr(allow_assignment=False))
        if res.error:
            return res

        element_nodes.append(first_element)
        while self.current_tok.type == TT_COMMA:
            res.register_advancement()
            self.advance()
            element_nodes.append(res.register(self.expr(allow_assignment=False)))
            if res.error:
                return res

        if self.current_tok.type != TT_RSQUARE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected ',' or ']'",
                )
            )
        res.register_advancement()
        self.advance()

        return res.success(
            ListNode(element_nodes, pos_start, self.current_tok.pos_end.copy())
        )

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None
        is_multiline_structure = False

        if not self.current_tok.matches(TT_KEYWORD, "if"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'if'",
                )
            )
        res.register_advancement()
        self.advance()

        condition = res.register(self.expr(allow_assignment=False))
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, "do"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'do'",
                )
            )
        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            is_multiline_structure = True
            res.register_advancement()
            self.advance()
            body = res.register(self.statements())
            if res.error:
                return res
            cases.append((condition, body, True))
        else:
            body = res.register(self.statement())
            if res.error:
                return res
            cases.append((condition, body, False))

        while self.current_tok.matches(TT_KEYWORD, "elif"):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr(allow_assignment=False))
            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, "do"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'do'",
                    )
                )
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                is_multiline_structure = True
                res.register_advancement()
                self.advance()
                body = res.register(self.statements())
                if res.error:
                    return res
                cases.append((condition, body, True))
            else:
                if is_multiline_structure:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Can't mix single-line and multi-line blocks in an if-elif-else chain",
                        )
                    )
                body = res.register(self.statement())
                if res.error:
                    return res
                cases.append((condition, body, False))

        if self.current_tok.matches(TT_KEYWORD, "else"):
            res.register_advancement()
            self.advance()

            if not self.current_tok.matches(TT_KEYWORD, "do"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'do'",
                    )
                )
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                is_multiline_structure = True
                res.register_advancement()
                self.advance()
                body = res.register(self.statements())
                if res.error:
                    return res
                else_case = (body, True)
            else:
                if is_multiline_structure:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Can't mix single-line and multi-line blocks in an if-elif-else chain",
                        )
                    )
                body = res.register(self.statement())
                if res.error:
                    return res
                else_case = (body, False)

        if is_multiline_structure:
            if not self.current_tok.matches(TT_KEYWORD, "done"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'done'",
                    )
                )
            res.register_advancement()
            self.advance()

        return res.success(IfNode(cases, else_case))

    def for_expr(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if not self.current_tok.matches(TT_KEYWORD, "for"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'for'",
                )
            )
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected identifier",
                )
            )

        first_var_name_tok = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_COMMA or self.current_tok.matches(
            TT_KEYWORD, "in"
        ):
            var_name_toks = [first_var_name_tok]
            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()
                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected identifier",
                        )
                    )
                var_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if not self.current_tok.matches(TT_KEYWORD, "in"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'in' after variable(s) in for-in loop",
                    )
                )

            res.register_advancement()
            self.advance()

            iterable_node = res.register(self.expr(allow_assignment=False))
            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, "do"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'do'",
                    )
                )
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                body = res.register(self.statements())
                if res.error:
                    return res
                if not self.current_tok.matches(TT_KEYWORD, "done"):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected 'done'",
                        )
                    )
                res.register_advancement()
                self.advance()
                return res.success(
                    ForInNode(
                        var_name_toks,
                        iterable_node,
                        body,
                        True,
                        pos_start,
                        body.pos_end,
                    )
                )

            body = res.register(self.statement())
            if res.error:
                return res
            return res.success(
                ForInNode(
                    var_name_toks, iterable_node, body, False, pos_start, body.pos_end
                )
            )

        elif self.current_tok.type == TT_EQ or self.current_tok.matches(
            TT_KEYWORD, "to"
        ):
            loop_specs = []
            var_name_tok = first_var_name_tok

            while True:
                start_value_node = None
                end_value_node = None
                step_value_node = None

                if self.current_tok.matches(TT_KEYWORD, "to"):
                    zero_tok = Token(
                        TT_INT, 0, var_name_tok.pos_start, var_name_tok.pos_end
                    )
                    start_value_node = NumberNode(zero_tok)

                    res.register_advancement()
                    self.advance()

                    end_value_node = res.register(self.expr(allow_assignment=False))
                    if res.error:
                        return res

                elif self.current_tok.type == TT_EQ:
                    res.register_advancement()
                    self.advance()
                    start_value_node = res.register(self.expr(allow_assignment=False))
                    if res.error:
                        return res

                    if not self.current_tok.matches(TT_KEYWORD, "to"):
                        return res.failure(
                            InvalidSyntaxError(
                                self.current_tok.pos_start,
                                self.current_tok.pos_end,
                                "Expected 'to'",
                            )
                        )
                    res.register_advancement()
                    self.advance()

                    end_value_node = res.register(self.expr(allow_assignment=False))
                    if res.error:
                        return res
                else:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected '=' or 'to'",
                        )
                    )

                if self.current_tok.matches(TT_KEYWORD, "step"):
                    res.register_advancement()
                    self.advance()
                    step_value_node = res.register(self.expr(allow_assignment=False))
                    if res.error:
                        return res

                loop_specs.append(
                    (var_name_tok, start_value_node, end_value_node, step_value_node)
                )

                if self.current_tok.type != TT_COMMA:
                    break

                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected identifier after ',' in for loop",
                        )
                    )
                var_name_tok = self.current_tok
                res.register_advancement()
                self.advance()

            if not self.current_tok.matches(TT_KEYWORD, "do"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'do'",
                    )
                )
            res.register_advancement()
            self.advance()

            is_multiline = False
            body_node = None
            if self.current_tok.type == TT_NEWLINE:
                is_multiline = True
                res.register_advancement()
                self.advance()
                body_node = res.register(self.statements())
                if res.error:
                    return res

                if not self.current_tok.matches(TT_KEYWORD, "done"):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected 'done'",
                        )
                    )
                res.register_advancement()
                self.advance()
            else:
                is_multiline = False
                body_node = res.register(self.statement())
                if res.error:
                    return res

            final_node = body_node
            for var, start, end, step in reversed(loop_specs):
                final_node = ForNode(var, start, end, step, final_node, is_multiline)

            return res.success(final_node)

        else:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'in', '=', or 'to' after for loop variable",
                )
            )

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "while"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    f"Expected 'while'",
                )
            )
        res.register_advancement()
        self.advance()

        condition = res.register(self.expr(allow_assignment=False))
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, "do"):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    f"Expected 'do'",
                )
            )
        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
            body = res.register(self.statements())
            if res.error:
                return res
            if not self.current_tok.matches(TT_KEYWORD, "done"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        f"Expected 'done'",
                    )
                )
            res.register_advancement()
            self.advance()
            return res.success(WhileNode(condition, body, True))

        body = res.register(self.statement())
        if res.error:
            return res
        return res.success(WhileNode(condition, body, False))

    def func_def(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if not self.current_tok.matches(TT_KEYWORD, "defun"):
            return res.failure(
                InvalidSyntaxError(
                    pos_start, self.current_tok.pos_end, "Expected 'defun'"
                )
            )
        res.register_advancement()
        self.advance()

        var_name_tok = None
        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()

        if self.current_tok.type != TT_LPAREN:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, "Expected '('"
                )
            )
        res.register_advancement()
        self.advance()

        arg_name_toks = []
        defaults = []
        vargs_name_tok = None
        kargs_name_tok = None
        parsing_stage = "args"

        while self.current_tok.type != TT_RPAREN:
            if self.current_tok.type == TT_MUL:
                if parsing_stage != "args":
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Unexpected '*'",
                        )
                    )
                res.register_advancement()
                self.advance()
                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected identifier after '*'",
                        )
                    )
                vargs_name_tok = self.current_tok
                parsing_stage = "vargs"
                res.register_advancement()
                self.advance()

            elif self.current_tok.type == TT_DOUBLE_STAR:
                if parsing_stage == "kargs":
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Unexpected '**'",
                        )
                    )
                res.register_advancement()
                self.advance()
                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected identifier after '**'",
                        )
                    )
                kargs_name_tok = self.current_tok
                parsing_stage = "kargs"
                res.register_advancement()
                self.advance()

            elif self.current_tok.type == TT_IDENTIFIER:
                if parsing_stage in ("vargs", "kargs"):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Positional argument cannot follow *vargs or **kargs",
                        )
                    )

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

                if self.current_tok.type == TT_EQ:
                    res.register_advancement()
                    self.advance()

                    default_value = res.register(self.expr(allow_assignment=False))
                    if res.error:
                        return res
                    defaults.append(default_value)
                else:
                    defaults.append(None)

            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected identifier, '*' or '**'",
                    )
                )

            if self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()
            elif self.current_tok.type != TT_RPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ',' or ')'",
                    )
                )

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_ARROW:
            res.register_advancement()
            self.advance()
            body = res.register(self.expr())
            if res.error:
                return res
            return res.success(
                FuncDefNode(
                    var_name_tok,
                    arg_name_toks,
                    defaults,
                    vargs_name_tok,
                    kargs_name_tok,
                    body,
                    True,
                    [],
                )
            )
        elif self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
            body = res.register(self.statements())
            if res.error:
                return res
            if not self.current_tok.matches(TT_KEYWORD, "done"):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected 'done' after function body",
                    )
                )
            res.register_advancement()
            self.advance()
            return res.success(
                FuncDefNode(
                    var_name_tok,
                    arg_name_toks,
                    defaults,
                    vargs_name_tok,
                    kargs_name_tok,
                    body,
                    False,
                    [],
                )
            )
        else:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected '->' or newline after function parameters",
                )
            )

    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_tok and (
            self.current_tok.type in ops
            or (self.current_tok.type, self.current_tok.value) in ops
        ):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            right = res.register(func_b())
            if res.error:
                return res

            left = BinOpNode(left, op_tok, right)

        return res.success(left)
```

## File: `src\utils.py`
```python
class Token:
    __slots__ = ["type", "value", "pos_start", "pos_end"]

    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            if self.type == "STRING":
                return (
                    f"STRING: '{self.value}'".replace("\n", "\\n")
                    .replace("\t", "\\t")
                    .replace("\r", "\\r")
                    .replace("\\", "\\\\")
                    if self.value.find("'") == -1
                    else f'STRING: "{self.value}"'.replace("\n", "\\n")
                    .replace("\t", "\\t")
                    .replace("\r", "\\r")
                    .replace("\\", "\\\\")
                )
            elif (
                self.value == "INT"
                or self.value == "FLOAT"
                or self.value == "IDENTIFIER"
                or self.value == "KEYWORD"
            ):
                return f"{self.type}: {self.value}"
            return f"{self.type}: {self.value}"
        return f"{self.type}"


class Position:
    __slots__ = ["idx", "ln", "fn", "ftxt"]

    def __init__(self, idx, ln, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        if current_char == "\n":
            self.ln += 1
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.fn, self.ftxt)


class RTResult:

    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue = False
        self.loop_should_break = False

    def register(self, res):
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.func_return_value = value
        return self

    def success_continue(self):
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
        return (
            self.error
            or self.func_return_value
            or self.loop_should_continue
            or self.loop_should_break
        )
```

## File: `tests\bakme.zyx`
```python
load "libs.ffio"
load "libs.sys"
load "libs.string"
load "libs.termcolor"

defun backup_folder(path, cbp, rbp)
    lf = ffio.list_dir(path)
    for i = 0 to len(lf) do
        f = lf$i
        flp = path + ffio.os_sep + f
        fbd = cbp + ffio.os_sep + f
        if flp == rbp do
            termcolor.cprintln("Skipping main backup directory itself: " + flp, "yellow", none, none)
            continue
        done
        if ffio.is_file(flp) do
            e = is_panic(ffio.copy, [flp, fbd + ".bak"])
            
            if is_none(e$1) do
                termcolor.cprintln("Backup created: " + fbd + ".bak", "green", none, none)
            else do
                ems = e$1 
                if string.startswith(ems, "File ") do
                    msg = slice(ems, len("File "), len(ems), none)
                    termcolor.cprintln(msg, "red", none, none)
                done
            done
        else do
            e = is_panic(ffio.make_dir, [fbd])
            if not is_none(e$1) do
                termcolor.cprintln("Error: Can not make subfolder in backup: " + fbd + " (Reason: " + (e$1) + ")", "red", none, none)
            else do
                backup_folder(flp, fbd, rbp)
            done
        done
    done
done

defun main()
    if len(sys.argv) < 2 do
        termcolor.cprintln("Usage: bakme.zyx <folder_to_backup>", "yellow", none, none)
        sys.exit(1)
    done
    fp = sys.argv$1
    if not ffio.exists(fp) do 
        termcolor.cprintln("Error: Folder does not exist: " + fp, "red", none, none) 
        sys.exit(1)
    done
    if ffio.is_file(fp) do 
        termcolor.cprintln("Error: Path provided is not a folder: " + fp, "red", none, none)
        sys.exit(1)
    done
    abrp = fp + ffio.os_sep + "backup"
    emmb = is_panic(ffio.make_dir, [abrp])
    if not is_none(emmb$1) do
        if ffio.exists(abrp) and not ffio.is_file(abrp) do
            termcolor.cprintln("Main backup folder already exists (and is a directory): " + abrp, "cyan", none, none)
        else do
            termcolor.cprintln("Error: Can not make main backup folder: " + abrp + " (Reason: " + (emmb$1) + ")", "red", none, none)
            sys.exit(1)
        done
    else do
        termcolor.cprintln("Main backup folder created: " + abrp, "blue", none, none)
    done
    termcolor.cprintln("Starting backup of: " + fp, "cyan", none, none)
    termcolor.cprintln("Target backup folder: " + abrp, "cyan", none, none)
    backup_folder(fp, abrp, abrp)
    termcolor.cprintln("Backup process finished.", "green", none, none)
done

if is_main do
    main()
done
```

## File: `tests\brainfuck.zyx`
```python
load "libs.sys"
load "libs.string"
load "libs.listm"

defun pass() -> none

defun brainfuck(nput)
    if not is_str(nput) do
        panic("'nput' must be a string", "T")
    done
    memory = [0]
    pointer = 0
    nput = string.split(nput, "")
    output = ""
    i = 0
    while i < len(nput) do
        c = nput$i
        # println("i: " + to_str(i) + ", " + "c: " + to_str(c) + ", " + "memory: " + to_str(memory) + ", " + "pointer: " + to_str(pointer))
        if (c) == ">" do
            if pointer+1 >= 30000 do
                println("Memory Error")
                return
            else do
                if pointer+1 >= len(memory) do
                    append(memory, 0)
                done
            done
            pointer += 1
        elif (c) == "<" do
            if pointer > 0 do
                pointer -= 1
            done
        elif (c) == "+" do
            memory$pointer = ((memory$pointer) + 1) % 256
        elif (c) == "-" do
            memory$pointer = ((memory$pointer) - 1)  % 256
        elif (c) == "." do
            output = output + string.chr(memory$pointer)
        elif (c) == "," do
            _in = input("> ")
            if len(_in) == 0 do
                memory$pointer = 0
            else do
                memory$pointer = string.ord(_in$0)
            done
        elif (c) == "[" do
            if (memory$pointer) == 0 do
                count = 1
                while count > 0 do
                    i += 1
                    c = nput$i
                    if i >= len(nput) do
                        println("Unmatched '['")
                        return
                    done
                    if (c) == "[" do
                        count += 1
                    elif (c) == "]" do
                        count -= 1
                    done
                done
            done
        elif (c) == "]" do
            if (memory$pointer) != 0 do
                count = 1
                while count > 0 do
                    i -= 1
                    c = nput$i
                    if i < 0 do
                        println("Unmatched ']'")
                        return
                    done
                    if (c) == "]" do
                        count += 1
                    elif (c) == "[" do
                        count -= 1
                    done
                done
            done
        done
        i += 1
    done
    return output
done

defun main()
    println("Brainfuck Interpreter (type 'quit' to exit).")
    while true do
        code = input(">> ")
        if string.strip(code, " ") == "quit" do
            sys.exit(0)
            return
        done
        output = brainfuck(code)
        if is_none(output) do
            continue
        elif len(output) == 0 do
            continue
        elif output$(-1) != "\n" do
            println(output)
        else do
            print(output)
        done
    done
done

if is_main do
    main()
done
```

## File: `tests\channel_test_1.zyx`
```python
load "libs.threading"
load "libs.channel"
load "libs.time"

println("--- Channel Demo ---")

messages = channel.new()

defun worker()
    println("  (Worker thread started)")
    time.sleep(2)
    println("  (Worker sending message: 'Hello from thread!')")
    channel.send(messages, "Hello from thread!")

    time.sleep(1)
    println("  (Worker sending message: 'Work done.')")
    channel.send(messages, "Work done.")
    println("  (Worker thread finished)")
done

println("Main: Starting worker thread...")
t = threading.start(worker)

println("Main: Waiting to receive a message...")
msg1 = channel.recv(messages)
println("Main: Received -> " + to_str(msg1))

println("Main: Waiting for the next message...")
msg2 = channel.recv(messages)
println("Main: Received -> " + to_str(msg2))

threading.join(t)
println("--- Demo Finished ---")
```

## File: `tests\channel_test_2.zyx`
```python
load "libs.threading"
load "libs.channel"
load "libs.time"

println("--- Producer/Consumer Demo ---")

messages = channel.new()

defun producer()
    for i = 1 to 5 do
        println("Producer: sending " + to_str(i))
        channel.send(messages, i)
        time.sleep(1)
    done
    println("Producer: finished sending")
done

defun consumer()
    for i = 1 to 5 do
        msg = channel.recv(messages)
        println("Consumer: received -> " + to_str(msg))
    done
    println("Consumer: finished receiving")
done

t1 = threading.start(producer)
t2 = threading.start(consumer)

threading.join(t1)
threading.join(t2)

println("--- Demo Finished ---")
```

## File: `tests\config_parser.zyx`
```python
load "libs.ffio"
load "libs.sys"
load "libs.string"
load "libs.listm"
load "libs.termcolor"

defun parse_config(config_file)
    parsed_config_data = []
    current_section_name = "__global__"
    current_section_items = []
    lines = string.split(ffio.read(config_file, "r"), "\n")
    for i to len(lines) do
        line = lines$i
        if line != "" do
            line = string.strip(line, " ")
            if string.startswith(line, "#") or string.startswith(line, ";") do
                continue
            done
        done
        if string.startswith(line, "[") do
            if len(current_section_items) > 0 or current_section_name != "__global__" do
                append(parsed_config_data, [current_section_name, current_section_items])
            done
            end_idx = listm.index_of(string.split(line, ""), "]")
            if end_idx == none do
                termcolor.cprint("Error", "red", none, "bold")
                println(": line " + to_str(i + 1) + " has malformed section (missing ']'). Skipping.")
                continue
            done
            raw_section_name = slice(line, 1, end_idx, none)
            current_section_name = string.strip(raw_section_name, " \t")
            if current_section_name == "" do
                termcolor.cprint("Warning", "yellow", none, "bold")
                println(": line " + to_str(i + 1) + " has an empty section name. Using '__empty_section__'.")
                current_section_name = "__empty_section__"
            done
            current_section_items = []
            continue
        done
        vals = string.split(line, "=")
        if len(vals) < 2 do
            termcolor.cprint("Warning", "yellow", none, "bold")
            println(": line " + to_str(i + 1) + " is not a valid config line or section header. Skipping.")
            continue
        done
        if len(vals) > 2 do
            termcolor.cprint("Error", "red", none, "bold")
            println(": line " + to_str(i + 1) + " has too many '=' for a key-value pair.")
            continue
        done
        key = string.strip(to_str(vals$0), " ")
        val_str_raw = string.strip(to_str(string.join("", slice(vals, 1, len(vals), none))), " ")
        if key == "" or val_str_raw == "" do
            termcolor.cprint("Error", "red", none, "bold")
            println(": line " + to_str(i + 1) + " has an empty key or value.")
            continue
        done
        val = val_str_raw 
        val_str_processed = val_str_raw
        if len(string.split(val_str_raw, "#")) > 1 or len(string.split(val_str_raw, ";")) > 1 do
            in_single_quote = false
            in_double_quote = false
            val_chars = string.split(val_str_raw, "")
            for char_idx to len(val_chars) do
                c = val_chars$char_idx
                if c == "'" and not in_double_quote do
                    in_single_quote = not in_single_quote
                elif c == '"' and not in_single_quote do
                    in_double_quote = not in_double_quote
                elif (c == '#' or c == ';') and not in_single_quote and not in_double_quote do
                    val_str_processed = string.strip(string.join("", slice(val_chars, 0, char_idx, none)), " ")
                    break
                done
            done
        done
        if is_num(to_int(val_str_processed, true)) do
            if string.endswith(to_str(to_float(val_str_processed, false)), ".0") do
                val = to_int(val_str_processed, false)
            else do
                val = to_float(val_str_processed, false)
            done
        elif val_str_processed == "none" do
            val = none
        elif val_str_processed == "true" do
            val = true
        elif val_str_processed == "false" do
            val = false
        elif (string.startswith(val_str_processed, '"') and string.endswith(val_str_processed, '"')) or (string.startswith(val_str_processed, "'") and string.endswith(val_str_processed, "'")) do
            val = to_str(slice(val_str_processed, 1, -1, none))
        else do
            val = to_str(val_str_processed)
        done
        append(current_section_items, [key, val])
    done
    if len(current_section_items) > 0 or current_section_name != "__global__" or len(parsed_config_data) == 0 do
        is_initial_global_and_empty = (current_section_name == "__global__" and len(current_section_items) == 0)
        if not (is_initial_global_and_empty and len(parsed_config_data) > 0) do 
            append(parsed_config_data, [current_section_name, current_section_items])
        done
    done
    return parsed_config_data
done

# --- Note --- #
# use this function to get value from config
# defun get_config_value(config_data, section_name, key_name, default_value)
#     for i to len(config_data) do
#         current_section = config_data$i
#         if current_section$0 == section_name do
#             items_in_section = current_section$1
#             for j to len(items_in_section) do
#                 kv_pair = items_in_section$j
#                 if kv_pair$0 == key_name do
#                     return kv_pair$1
#                 done
#             done
#             return default_value
#         done
#     done
#     return default_value
# done
# --- Note --- #

defun main()
    if len(sys.argv) < 2 do
        termcolor.cprintln("Usage: script_name <config_file_path>", "yellow", none, "bold")
        sys.exit(1)
    done
    config_path = sys.argv$1
    if not ffio.exists(config_path) do
        termcolor.cprintln("Error: File does not exist: " + config_path, 'red', none, 'bold')
        sys.exit(1)
    done
    if not ffio.is_file(config_path) do
        termcolor.cprintln("Error: Path is not a file: " + config_path, 'red', none, 'bold')
        sys.exit(1)
    done
    termcolor.cprintln("Parsing configuration file: " + config_path, "cyan", none, none)
    config_data = parse_config(config_path)
    if len(config_data) == 0 do
        termcolor.cprintln("No configuration entries found or file is effectively empty.", "yellow")
    else do
        println("\n--- Parsed Configuration ---")
        for i to len(config_data) do
            section_block = config_data$i
            section_name = section_block$0
            section_items = section_block$1
            termcolor.cprint("[", "yellow", none, "bold")
            termcolor.cprint(to_str(section_name), "yellow", none, "bold")
            termcolor.cprintln("]", "yellow", none, "bold")
            if len(section_items) == 0 do
                termcolor.cprintln("  (empty section)", "grey", none, none)
            else do
                for j to len(section_items) do
                    kv_pair = section_items$j
                    key = kv_pair$0
                    value = kv_pair$1
                    print("  ")
                    termcolor.cprint(to_str(key), 'magenta', none, 'bold')
                    print(" = ")
                    termcolor.cprint(to_str(value), 'green', none, none)
                    print(" (type: ")
                    termcolor.cprint(type(value), "blue", none, none)
                    println(")")
                done
            done
            if i < len(config_data) - 1 do
                println("")
            done
        done
        # ---  Example --- #
        # println("\n--- Example Get Config Value ---")
        # assuming you have a config file like:
        # name = GlobalVal
        # [Settings]
        # user = Alice
        # theme = dark
        # [Database]
        # host = localhost
        # user_name = get_config_value(config_data, "Settings", "user", "default_user")
        # termcolor.cprint("User from [Settings]: ", "white", none, none)
        # termcolor.cprintln(user_name, "cyan", none, none)
        # db_host = get_config_value(config_data, "Database", "host", "127.0.0.1")
        # termcolor.cprint("Host from [Database]: ", "white", none, none)
        # termcolor.cprintln(db_host, "cyan", none, none)
        # global_val = get_config_value(config_data, "__global__", "name", "not_found")
        # termcolor.cprint("Name from __global__: ", "white", none, none)
        # termcolor.cprintln(global_val, "cyan", none, none)
        # missing_val = get_config_value(config_data, "Settings", "nonexistent", "MISSING")
        # termcolor.cprint("Missing from [Settings]: ", "white", none, none)
        # termcolor.cprintln(missing_val, "red", none, none)
        # --- Example --- #
    done
done

if is_main do
    main()
done
```

## File: `tests\csv_parser.zyx`
```python
load "libs.sys"
load "libs.ffio"
load "libs.csv"

if len(sys.argv) != 2 do
    println("Usage: " + ffio.abs_path(sys.argv$0) + " <your-csv-file>")
    sys.exit(1)
done

if not ffio.exists(sys.argv$1) do
    println('File not found: "' + ffio.abs_path(sys.argv$1) + '"')
    sys.exit(1)
done

r = csv.read(sys.argv$1)

println("r = " + to_str(r))
```

## File: `tests\decorator_test_1.zyx`
```python
defun log_call(fn)
    defun wrapper(*vargs, **kargs)
        println("Calling function: " + slice(to_str(fn), 10, -1))
        result = fn(*vargs, **kargs)
        println("Function " + slice(to_str(fn), 10, -1) + " finished.")
        return result
    done
    return wrapper
done

&log_call
defun add(a, b) -> a + b

add(5, 3)

logger("Processing Data:", 101, "active", user="memeviber", status="online")
```

## File: `tests\decorator_test_2.zyx`
```python
load "libs.decorators"

&decorators.cache
defun fib(n)
    if n < 2 do
        return n
    done
    a = 0
    b = 1
    for i = 1 to n do
        temp = b
        b = a + b
        a = temp
    done
    return b
done
println("Fib(40) with cache...")
&decorators.measure_time
defun cached_fib() -> fib(40)
println(cached_fib())
println(cached_fib())

counter = 0
&decorators.retry(3)
defun might_fail()
    using counter
    counter += 1
    if counter < 3 do
        panic("Network failed!")
    done
    return "Success on attempt " + to_str(counter)
done
println(might_fail())

&decorators.ignore_error(default=0)
defun risky(a, b) -> a / b
println("Result of risky function: " + to_str(risky(4, 2)))
println("Result of risky function: " + to_str(risky(1, 0)))

```

## File: `tests\donut.zyx`
```python
load "libs.sys"
load "libs.math"
load "libs.string"
load "libs.time"
load "libs.memory"
load "libs.keyboard"

A = 0
B = 0
sin_ = math.sin # get member beforehand to avoid overhead
cos_ = math.cos # get member beforehand to avoid overhead
loop_count = 0
max_loop = to_int(2 * math.PI / 0.04, false) # 157 frames
shading = [".", ",", "-", "~", ":", ";", "=", "!", "*", "#", "$", "@"]
print(string.chr(27) + "[2J" + string.chr(27) + "[H")
while true do
    frame_id = "frame_" + to_str(loop_count)
    cached = memory.recall(frame_id)
    if loop_count > max_loop do
        loop_count = 0
        A = 0
        B = 0
        continue
    else do
        if cached != none do
            print(string.chr(27) + "[2J" + string.chr(27) + "[H")
            println(cached)
            println("\n\nPress q to exit...")
            time.sleep(0.03)
            if keyboard.is_pressed("q") do
                print(string.chr(27) + "[2J" + string.chr(27) + "[H")
                sys.exit()
            done
        else do
            print("Rendering donut... (" + to_str(loop_count) + "/" + to_str(max_loop) + " frames)\r")
            z = [0] * 1760
            b = [" "] * 1760
            for j = 0 to 628 step 7 do
                for i = 0 to 628 step 2 do
                    c = sin_(i / 100)
                    d = cos_(j / 100)
                    e = sin_(A)
                    f = sin_(j / 100)
                    g = cos_(A)
                    h = d + 2
                    D = 1 / (c * h * e + f * g + 5)
                    l = cos_(i / 100)
                    m = cos_(B)
                    n = sin_(B)
                    t = c * h * g - f * e
                    x = to_int(40 + 30 * D * (l * h * m - t * n), false)
                    y = to_int(12 + 15 * D * (l * h * n + t * m), false)
                    o = x + 80 * y
                    N = to_int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n), false)
                    if o >= 0 and o < 1760 and y < 22 and y > 0 and x > 0 do
                        z_val = z$o
                        if D > z_val do
                            z$o = D
                            char = if N > 0 do shading$N else do shading$0
                            b$o = char
                        done
                    done
                done
            done
            frame_str = ""
            for i = 0 to 1759 do
                frame_str = frame_str + (b$i)
                if i % 80 == 79 do
                    frame_str = frame_str + "\n"
                done
            done
            memory.remember(frame_id, frame_str)
        done
        loop_count += 1
    done
    A += 0.04
    B += 0.08
done
```

## File: `tests\guess_number.zyx`
```python
load "libs.random"
load "libs.sys"

a = 0
ma = 10
sn = 0

defun handle_input(m, m_)
    i = to_int(input("Enter a number from " + to_str(m) + " to " + to_str(m_) + ": "), true)
    while i == none or (i < m or i > m_) do
        a += 1
        if a >= ma do
            println("You have used all your attempts!\nThe secret number was: " + to_str(sn))
            sys.exit(1)
        done
        println("Invalid input!")
        i = to_int(input("Enter a number from " + to_str(m) + " to " + to_str(m_) + ": "), true)
    done
    return i
done

defun guess_number(m, m_)
    using sn
    a = 0
    sn = random.rand_int(m, m_)
    while a < ma do
        i = handle_input(m, m_)
        a += 1
        if i == sn do
            println("You guessed it right!\nAttempts: " + to_str(a))
            return none
        elif i < sn do
            println("Your guess is lower than the secret number!")
        else do
            println("Your guess is higher than the secret number!")
        done
    done
    println("You have used all your attempts!\nThe secret number was: " + to_str(sn))
done

defun main()
    m = 1
    m_ = 100
    guess_number(m, m_)
done

if is_main do
    main()
done
```

## File: `tests\json_parser.zyx`
```python
load "libs.sys"
load "libs.ffio"
load "libs.json"

if len(sys.argv) != 2 do
    println("Usage: " + ffio.abs_path(sys.argv$0) + " <your-json-file>")
    sys.exit(1)
done

if not ffio.exists(sys.argv$1) do
    println('File not found: "' + ffio.abs_path(sys.argv$1) + '"')
    sys.exit(1)
done

j = ffio.read(sys.argv$1, "r")
r = json.parse(j)

println("r = " + to_str(r))
```

## File: `tests\magic.zyx`
```python
# https://memeviber.github.io/Zerionyx/docs.html#zen-of-zerionyx

a = 1
b = 2
c = 3
x = 4
y = 5
z = 6

# yes
result = (
    x
    + y * z
    - a / b ^ 2
)

# no
result = x \
    + y * z \
    - a / b ^ 2 \

# yes
if x > 10 \
    and y < 5 \
    or z == 99 do
    println("yes")
done

# no
if (
        x > 10
        and y < 5
        or z == 99
    ) do
    println("no")
done

# yes
if x < y do
    println("x is less than y")
elif x > y do
    println("x is greater than y")
done

# no
if x < y do


    println("x is less than y")



elif x > y do

    println("x is greater than y")


done

# no
if x < y do
                            println("x is less than y")
elif x > y do
   println("x is greater than y")
done

# yes
temp_file = "temp.txt"

# no 
t = "temp.txt"

# yes
a = 1
b = a + a

# no
_ = 1
__ = _ + _
```

## File: `tests\matrix.zyx`
```python
load "libs.random"
load "libs.sys"
load "libs.string"

clear()
if sys.os_name == "nt" do sys.system("color 02")

while true do
    lst = []
    for _ to 148 do # IDK =)))
        append(lst, random.rand_int(0, 1))
    done
    print(string.join("", lst))
done
```

## File: `tests\outer.zyx`
```python
x = 2

defun outer()
    x = 0
    defun inter()
        using parent x
        x += 1
    done
    println(x)
    inter()
    println(x)
done

outer()
println(x)
```

## File: `tests\speed_test.zyx`
```python
load "libs.time"
load "libs.sys"

N = 100000000
repeats = 10
times = []

for r = 1 to repeats + 1 do
    total = 0
    start = time.time()
    for i = 1 to N + 1 do
        total += i
    done
    end = time.time()
    append(times, end - start)
done

sum = 0
fastest = (times$0)
slowest = (times$0)

for t in times do
    sum += t
    if t < fastest do
        fastest = t
    done
    if t > slowest do
        slowest = t
    done
done

avg = sum / to_float(len(times))

println("Average: " + to_str(avg)     + " s")
println("Fastest: " + to_str(fastest) + " s")
println("Slowest: " + to_str(slowest) + " s")

# Zerionyx executed on Python 3.12.8 (64-bit) on AMD Ryzen 7 4800H laptop (plugged-in mode):
# Average: 6.663556218147278 s
# Fastest: 6.343989849090576 s
# Slowest: 7.311691522598267 s

# Zerionyx executed on PyPy 3.11 (v7.3.19, 64-bit, JIT enabled) on AMD Ryzen 7 4800H laptop (plugged-in mode):
# Average: 0.385618782043457 s
# Fastest: 0.343375682830810 s
# Slowest: 0.444282054901123 s
```

## File: `tests\test.zyx`
```python
# Hello World
println("Hello, World!")
print("Hello, World!\n")

# Arithmetic
x = 10
y = 20
println(x + y)
println(x - y)
println(x * y)
println(x / y)
println(x % y)
println(x // y)
println(x ^ y)

# Function definition
defun add(a, b)
    return a + b
done

# One-line function
defun add(a, b) -> a += b

println(add(5, 3))

# Lists
nums = [1, 2, 3, 4, 5]
append(nums, 6)
println(nums)
println(nums$0)
println(nums$5)

# HashMaps
users = []
append(users, {})
users$0$"name" = "user-1"
users$0$"password" = "123456"
println(users)
println(users$0$"name")
println(users$0$"password")

# Bytes
str_enc = to_bytes("Hello, World!")
println(to_str(str_enc))
println(str_enc$0)
println(str_enc$4)

# PyObject
os = pyexec("import os", {})
println(type(os))
r = pyexec("os.system('echo Hello, World!')", os)

# CFloat
tcf = to_cfloat
lst = [tcf("1/9")] * 9
x = tcf(0)
for i in lst do
    x += i
done
println(x == 1)

# Conditional
if x > y do
    println("X is greater")
elif x < y do
    println("Y is greater")
else do
    println("X is equals to Y")
done

# For-in loop
for i in nums do
    println(i)
done

# For loop
for i = 1 to 11 do
    println(i)
done

# While loop
a = 1
while a > 100 do
    a += 1
done
println(a)

# NameSpace
namespace m
    pi = 3.14
    defun area(r) -> pi * r * r
done
println(m.area(5))
```

## File: `tests\thread_pool_test.zyx`
```python
load "libs.threading"

defun my_func(name) -> "Hello, " + name
handle = threading.start(my_func, ["World"])
threading.join(handle)

pool = threading.pool.new(3)
for i in ["ThreadPool1", "ThreadPool2", "ThreadPool3", "ThreadPool4"] do
    future = threading.pool.submit(pool, my_func, [i])
    result = threading.pool.result(future)
    println(result)
done
threading.pool.shutdown(pool)
println(threading.pool.is_done(future))
```

## File: `tests\user_management_system.zyx`
```python
load "libs.hash"

users = []
current_user = none

defun hash_password(password) -> hash.sha256(to_bytes(password))

defun sign_up()
    user_name = input("Enter your name: ")
    hashed_password = hash_password(get_password("Enter your password: "))
    r = false
    for user in users do
        if user$"user_name" == user_name do
            println("User name already exists")
            input("Press enter to continue...")
            return
        done
    done
    append(users, {"user_name": user_name, "hashed_password": hashed_password})
    println("User created successfully")
    input("Press enter to continue...")
done

defun log_in()
    using current_user
    if current_user != none do
        println("You are already logged in as " + current_user)
        input("Press enter to continue...")
        return
    done
    user_name = input("Enter your user name: ")
    hashed_password = hash_password(get_password("Enter your password: "))
    found = false
    for user in users do
        if user$"user_name" == user_name and user$"hashed_password" == hashed_password do
            println("Login successful")
            current_user = user$"user_name"
            found = true
            break
        done
    done
    if not found do
        println("Invalid user name or password")
    done
    input("Press enter to continue...")
done

defun log_out()
    using current_user
    if current_user == none do
        println("You are not logged in")
    else do
        current_user = none
        println("Logged out successfully")
    done
    input("Press enter to continue...")
done

defun main()
    while true do
        clear()
        println("Welcome to the user management system (" + to_str(current_user) + ")")

        if current_user == none do
            println("1. Sign up")
            println("2. Log in")
            println("3. Exit")

            choice = to_int(input("Enter your choice: "), true)

            if choice == 1 do
                sign_up()
            elif choice == 2 do
                log_in()
            elif choice == 3 do
                break
            else do
                println("Invalid choice")
                input("Press enter to continue...")
            done

        else do
            println("1. Log out")
            println("2. Exit")

            choice = to_int(input("Enter your choice: "), true)

            if choice == 1 do
                log_out()
            elif choice == 2 do
                break
            else do
                println("Invalid choice")
                input("Press enter to continue...")
            done
        done
    done
done

if is_main do
    main()
done
```

## File: `tests\xor.zyx`
```python
load "libs.string"

defun xor_encrypt_decrypt(data, key)
    key_len = len(key)
    result = to_bytes("")
    for i to len(data) do
        result += to_bytes(bitwise_xor(data$i, key$(i % key_len)))
    done
    return result
done

plaintext = to_bytes("Hello Zerionyx!")
println("Plaintext: " + to_str(plaintext))

key = to_bytes("KY8")
println("Key: " + to_str(key))

ciphertext = xor_encrypt_decrypt(plaintext, key)
println("Ciphertext: " + to_str(ciphertext))

decrypted = xor_encrypt_decrypt(ciphertext, key)
println("Decrypted: " + to_str(decrypted))

for i in decrypted do
    print(string.chr(i))
done
print("\n")

```

## File: `zerionyx.py`
```python
import atexit
import io
import os
import shutil
import sys
import tempfile
import zipfile
from typing import TYPE_CHECKING

from src.interp import INFO, Fore, Style, run

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

if os.name != "nt" and not TYPE_CHECKING:
    try:
        import readline

        readline.parse_and_bind(r'"\e[A": history-search-backward')
        readline.parse_and_bind(r'"\e[B": history-search-forward')
        readline.parse_and_bind(r'"\e[C": forward-char')
        readline.parse_and_bind(r'"\e[D": backward-char')
    except ImportError:
        pass

MAGIC = b"ZEX-[</>]?"
MANIFEST_NAME = "__main__.zex.manifest"
_temp_dirs_to_clean = []
G = """

PROGRAM ::= STATEMENTS

STATEMENTS ::= STATEMENT (NEWLINE+ STATEMENT)* NEWLINE*

STATEMENT ::= SIMPLE_STATEMENT | COMPOUND_STATEMENT

SIMPLE_STATEMENT ::=
    "load" STRING
  | "return" [EXPR]
  | "continue"
  | "break"
  | "using" ["parent"] IDENTIFIER ("," IDENTIFIER)*
  | "del" IDENTIFIER ("," IDENTIFIER)*
  | EXPR

COMPOUND_STATEMENT ::=
    IF_EXPR
  | FOR_EXPR
  | WHILE_EXPR
  | NAMESPACE_EXPR
  | (DECORATOR+ DEF_FUNC)
  | DEF_FUNC

BODY ::= STATEMENT | (NEWLINE STATEMENTS "done")

EXPR ::= ASSIGNMENT_EXPR

ASSIGNMENT_EXPR ::=
    (IDENTIFIER AUG_ASSIGN_OP EXPR)
  | LOGIC_EXPR

AUG_ASSIGN_OP ::= "+=" | "-=" | "*=" | "/=" | "//=" | "%=" | "^="

LOGIC_EXPR ::= COMP_EXPR (("and" | "or") COMP_EXPR)*

COMP_EXPR ::=
    "not" COMP_EXPR
  | ARITH_EXPR (("==" | "!=" | "<" | ">" | "<=" | ">=") ARITH_EXPR)*

ARITH_EXPR ::= TERM (("+" | "-") TERM)*

TERM ::= FACTOR (("*" | "/" | "//" | "%") FACTOR)*

FACTOR ::=
    "-" FACTOR
  | "*" FACTOR                      (* vargs unpacking *) 
  | "**" FACTOR                     (* kargs unpacking *)
  | DOLLAR_EXPR

DOLLAR_EXPR ::= POWER ("$" POWER)*  (* $ is for indexing instead of [] *)

POWER ::= CALL ("^" FACTOR)*        (* power operator *)

CALL ::= ATOM ( ("." IDENTIFIER) | ("(" [ARG_LIST] ")") )*

ARG_LIST ::= ARG ("," ARG)*

ARG ::= EXPR | (IDENTIFIER "=" EXPR)

ATOM ::=
    INT | FLOAT | STRING | IDENTIFIER
  | "(" EXPR ")"
  | LIST_EXPR
  | HASHMAP_EXPR
  | IF_EXPR
  | FOR_EXPR
  | WHILE_EXPR
  | DEF_FUNC
  | NAMESPACE_EXPR

LIST_EXPR ::= "[" [EXPR ("," EXPR)*] "]"

HASHMAP_EXPR ::= "{" [EXPR ":" EXPR ("," EXPR ":" EXPR)*] "}"

NAMESPACE_EXPR ::= "namespace" IDENTIFIER NEWLINE STATEMENTS "done"

IF_EXPR ::=
    "if" EXPR "do" BODY
    ("elif" EXPR "do" BODY)*
    ["else" "do" BODY]?

FOR_EXPR ::=
    ("for" FOR_IN_CLAUSE | FOR_RANGE_CLAUSES) "do" BODY

FOR_IN_CLAUSE ::= IDENTIFIER ("," IDENTIFIER)* "in" EXPR

FOR_RANGE_CLAUSES ::= FOR_RANGE_CLAUSE ("," FOR_RANGE_CLAUSE)*

FOR_RANGE_CLAUSE ::= IDENTIFIER ["=" EXPR] "to" EXPR ["step" EXPR]

WHILE_EXPR ::= "while" EXPR "do" BODY

DECORATOR ::= "&" EXPR NEWLINE*

DEF_FUNC ::=
    "defun" [IDENTIFIER] "(" [PARAM_LIST] ")" ("->" EXPR | (NEWLINE STATEMENTS "done"))

PARAM_LIST ::= (PARAMS ["," VAR_PARAMS]) | VAR_PARAMS

PARAMS ::= PARAM ("," PARAM)*

PARAM ::= IDENTIFIER ["=" EXPR]

VAR_PARAMS ::= (VARARGS_PARAM ["," KWARGS_PARAM]) | KWARGS_PARAM

VARARGS_PARAM ::= "*" IDENTIFIER

KWARGS_PARAM ::= "**" IDENTIFIER

"""
L = """

MIT License

WARNING: This project contains code adapted from multiple public sources.

Some components are originally based on David Callanan's interpreter tutorial (2019),
licensed under the MIT License. Other parts are believed to derive from Fus3n's version,
which did not include an explicit license but was publicly shared for free use and modification.

Only modifications made by MemeViber are explicitly claimed under copyright.
Reasonable efforts have been made to trace original authors.
If you are an original author and believe attribution or licensing is missing,
please contact MemeViber.

Credits:
- David Callanan (2019, original author)
- Fus3n (2022, based on David Callanan's version)
- angelcaru (2024, modified David Callanan's version)
- MemeViber (2025-2026, further modified Fus3n's version, with some code adapted from angelcaru's version)

Copyright (c) 2019–2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


def cleanup_temp_dirs():
    for path in _temp_dirs_to_clean:
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except OSError:
                pass


atexit.register(cleanup_temp_dirs)


def pack_zex(output_file, main_script, other_files):
    if not output_file.endswith(".zex"):
        print(
            f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}Output file must have a '.zex' extension{Fore.RESET}{Style.RESET_ALL}"
        )
        return

    all_files = [main_script] + other_files
    for f in all_files:
        if not os.path.isfile(f):
            print(
                f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}Input file '{os.path.abspath(f)}' not found{Fore.RESET}{Style.RESET_ALL}"
            )
            return

    try:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(MANIFEST_NAME, os.path.basename(main_script))

            for f in all_files:
                filename = os.path.basename(f)

                if f.endswith(".zyx"):
                    with open(f, "r", encoding="utf-8") as file:
                        content = file.read()

                    lines = content.splitlines()
                    processed_lines = [line.strip() for line in lines if line.strip()]
                    processed_content = ";".join(processed_lines)

                    zf.writestr(filename, processed_content.encode("utf-8"))

                else:
                    with open(f, "rb") as file:
                        binary_content = file.read()
                    zf.writestr(filename, binary_content)

        with open(output_file, "wb") as f:
            f.write(MAGIC)
            f.write(zip_buffer.getvalue())

        print(f"{Fore.GREEN}Successfully packed to '{output_file}'{Fore.RESET}")

    except Exception as e:
        print(
            f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Packing Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}{e}{Fore.RESET}"
        )


def run_zex(file_path):
    temp_dir = tempfile.mkdtemp(prefix="zex_")
    _temp_dirs_to_clean.append(temp_dir)

    try:
        with open(file_path, "rb") as f:
            if f.read(len(MAGIC)) != MAGIC:
                print(
                    f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}Not a valid .zex file (invalid magic byte){Fore.RESET}{Style.RESET_ALL}"
                )
                sys.exit(1)

            with zipfile.ZipFile(f) as zf:
                if MANIFEST_NAME not in zf.namelist():
                    print(
                        f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}Manifest '{MANIFEST_NAME}' not found in the .zex archive{Fore.RESET}{Style.RESET_ALL}"
                    )
                    sys.exit(1)

                main_script_name = zf.read(MANIFEST_NAME).decode("utf-8").strip()

                zf.extractall(temp_dir)

                main_script_path = os.path.join(temp_dir, main_script_name)

                if not os.path.isfile(main_script_path):
                    print(
                        f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}Main script '{main_script_name}' specified in manifest not found in archive{Fore.RESET}{Style.RESET_ALL}"
                    )
                    sys.exit(1)

                with open(main_script_path, "r", encoding="utf-8") as file:
                    text = file.read()

                text = text.splitlines()
                for i in range(len(text)):
                    text[i] = text[i].strip()

                result, error = run(main_script_path, "\n".join(text))

                if error:
                    if hasattr(error, "as_string"):
                        print(f"{error.as_string()}")
                    else:
                        print(f"{error}")
                    sys.exit(1)
                elif result:
                    if len(result.value) == 1:
                        print(f"{repr(result.value[0])}")
                    else:
                        print(f"{repr(result)}")

    except zipfile.BadZipFile:
        print(
            f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}Invalid or corrupted .zex archive{Fore.RESET}{Style.RESET_ALL}"
        )
        sys.exit(1)
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(
            f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Interpreter Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}{e}{Fore.RESET}"
        )
        sys.exit(1)
    finally:
        if temp_dir in _temp_dirs_to_clean:
            _temp_dirs_to_clean.remove(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)


def check_file_comments_or_empty(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        all_empty_or_comments = True

        for line in lines:
            if not (
                line.strip() == ""
                or line.strip().startswith("#")
                or all(char == ";" for char in line.strip())
            ):
                all_empty_or_comments = False
                break
        if all_empty_or_comments:
            print(
                f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}The file is empty or only contains comments{Fore.RESET}{Style.RESET_ALL}"
            )
            sys.exit(0)


def main():
    if len(sys.argv) == 1:
        print(f"Zerionyx {INFO}")
        print(
            "Type 'grammar', 'copyright', 'credits', 'license', 'docs' for more information or 'exit' to exit."
        )
        try:
            while True:
                text = input(f"{Fore.LIGHTMAGENTA_EX}>>> {Fore.RESET}")
                if (
                    text.strip() == ""
                    or all(char == ";" for char in text.strip())
                    or text.strip().startswith("#")
                ):
                    continue
                if text.strip() == "exit":
                    print("exit...")
                    break
                if text.strip() == "grammar":
                    print(
                        ("=" * 96)
                        + G
                        + ("=" * 96)
                        + "\n\nPlease scroll up to read from the beginning.\n"
                    )
                    continue
                if text.strip() == "license":
                    print(
                        ("=" * 96)
                        + L
                        + ("=" * 96)
                        + "\n\nPlease scroll up to read from the beginning.\n"
                    )
                    continue
                if text.strip() == "copyright":
                    print("Copyright (c) 2019-2025\nAll Rights Reserved.")
                    continue
                if text.strip() == "credits":
                    print(
                        "Credits:\n- David Callanan (2019, original author)\n- Fus3n (2022, based on David Callanan's version)\n- angelcaru (2024, modified David Callanan's version)\n- MemeViber (2025-2026, further modified Fus3n's version, with some code adapted from angelcaru's version)"
                    )
                    continue
                if text.strip() == "docs":
                    print(
                        "Documentation: https://memeviber.github.io/Zerionyx/docs.html"
                    )
                    continue
                result, error = run("<stdin>", text)
                if error:
                    if hasattr(error, "as_string"):
                        print(f"{error.as_string()}")
                    else:
                        print(f"{error}")
                elif result:
                    if len(result.value) == 1:
                        print(f"{repr(result.value[0])}")
                    else:
                        print(f"{repr(result)}")
        except KeyboardInterrupt:
            print("\nexit...")
        except EOFError:
            print("exit...")
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(
                f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Interpreter Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}{e}{Fore.RESET}"
            )
    elif len(sys.argv) > 1 and sys.argv[1] == "--pack":
        if len(sys.argv) < 4:
            print(
                f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Usage{Fore.RESET}{Style.RESET_ALL}: {os.path.basename(sys.argv[0])} --pack <output.zex> <main_script.zyx> [other_files...]"
            )
            return
        output_file = sys.argv[2]
        main_script = sys.argv[3]
        try:
            other_files = sys.argv[4:]
        except IndexError:
            other_files = []
        pack_zex(output_file, main_script, other_files)
        return
    elif len(sys.argv) == 2 and sys.argv[1] == "--version":
        print(f"Zerionyx {INFO}")
        return
    else:
        file_name = os.path.abspath(sys.argv[1])

        if not file_name.endswith((".zyx", ".zex")):
            print(
                f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}The file must have a '.zyx' or '.zex' extension{Fore.RESET}{Style.RESET_ALL}"
            )
            return

        if not os.path.isfile(file_name) or not os.path.exists(file_name):
            print(
                f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}File '{os.path.abspath(file_name)}' does not exist{Fore.RESET}{Style.RESET_ALL}"
            )
            return

        if file_name.endswith(".zex"):
            run_zex(file_name)
            return

        try:
            check_file_comments_or_empty(file_name)
            with open(file_name, "r", encoding="utf-8") as file:
                text = file.read()
            text = text.splitlines()
            for i in range(len(text)):
                text[i] = text[i].strip()
            result, error = run(file_name, "\n".join(text))
            if error:
                if hasattr(error, "as_string"):
                    print(f"{error.as_string()}")
                else:
                    print(f"{error}")
                sys.exit(1)
            elif result:
                if len(result.value) == 1:
                    print(f"{repr(result.value[0])}")
                else:
                    print(f"{repr(result)}")
        except IOError as e:
            print(
                f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}{e}{Fore.RESET}"
            )
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(
                f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Interpreter Error{Fore.RESET}{Style.RESET_ALL}: {Fore.MAGENTA}{e}{Fore.RESET}"
            )
            return


if __name__ == "__main__":
    main()
```

## File: `zerionyx_lexer.py`
```python
# zerionyx_lexer.py

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import (
    Text,
    Comment,
    Operator,
    Keyword,
    Name,
    String,
    Number,
    Punctuation,
)


class ZerionyxLexer(RegexLexer):
    name = "Zerionyx"
    aliases = ["zerionyx", "zyx"]
    filenames = ["*.zyx", "*.zex"]

    zyx_keywords = (
        "and",
        "or",
        "not",
        "if",
        "elif",
        "else",
        "for",
        "to",
        "do",
        "step",
        "while",
        "defun",
        "done",
        "return",
        "continue",
        "break",
        "load",
        "in",
        "del",
        "namespace",
        "using",
        "parent",
    )

    zyx_constants = ("true", "false", "none", "PI", "E", "ln2", "nan", "inf", "neg_inf")

    zyx_builtins = (
        "println",
        "print",
        "input",
        "get_password",
        "clear",
        "type",
        "is_none",
        "is_num",
        "is_bool",
        "is_str",
        "is_list",
        "is_func",
        "is_thread",
        "is_thread_pool",
        "is_future",
        "is_namespace",
        "is_channel",
        "is_cfloat",
        "is_py_obj",
        "is_nan",
        "is_panic",
        "len",
        "panic",
        "pop",
        "append",
        "insert",
        "extend",
        "slice",
        "to_str",
        "to_int",
        "to_float",
        "to_cfloat",
        "to_bytes",
        "pyexec",
        "clone",
        "keys",
        "values",
        "items",
        "has",
        "get",
        "del_key",
        "get_member",
        "shl",
        "shr",
        "bitwise_and",
        "bitwise_or",
        "bitwise_xor",
        "bitwise_not",
    )

    zyx_types = (
        "list",
        "str",
        "int",
        "float",
        "func",
        "bool",
        "hashmap",
        "thread",
        "bytes",
        "py_obj",
        "cfloat",
        "namespace",
        "channel_type",
        "thread_pool_type",
        "future_type",
        "none_type",
    )

    tokens = {
        "root": [
            (r"\s+", Text),
            (r"#.*$", Comment.Single),
            (r"&[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*", Name.Decorator),
            (r"(defun)(\s+)([a-zA-Z_]\w*)", bygroups(Keyword, Text, Name.Function)),
            (
                r"(namespace)(\s+)([a-zA-Z_]\w*)",
                bygroups(Keyword.Namespace, Text, Name.Namespace),
            ),
            (r"(load)(\s+)", bygroups(Keyword.Namespace, Text), "load_string"),
            (words(zyx_keywords, suffix=r"\b"), Keyword),
            (words(zyx_constants, suffix=r"\b"), Keyword.Constant),
            (words(zyx_builtins, suffix=r"\b"), Name.Builtin),
            (words(zyx_types, suffix=r"\b"), Name.Builtin.Pseudo),
            (r'"""', String.Double, "string_double_multiline"),
            (r"'''", String.Single, "string_single_multiline"),
            (r'"', String.Double, "string_double"),
            (r"'", String.Single, "string_single"),
            (r"\d+\.\d+", Number.Float),
            (r"\d+", Number.Integer),
            (
                r"(\+=|-=|\*=|/=|//=|%=|\^=|==|!=|<=|>=|<|>|\+|-|\*|//|/|%|\^|\$|=)",
                Operator,
            ),
            (r"[.,:;(){}\[\]\\]", Punctuation),
            (r"[a-zA-Z_]\w*", Name),
        ],
        "load_string": [
            (r'"[^"]*"', String.Double, "#pop"),
            (r"'[^']*'", String.Single, "#pop"),
            (r"\s+", Text),
            (r"", Text, "#pop"),
        ],
        "string_double_multiline": [
            (r'[^"\\]+', String.Double),
            (r"\\.", String.Escape),
            (r'"""', String.Double, "#pop"),
            (r'"', String.Double),
        ],
        "string_single_multiline": [
            (r"[^'\\]+", String.Single),
            (r"\\.", String.Escape),
            (r"'''", String.Single, "#pop"),
            (r"'", String.Single),
        ],
        "string_double": [
            (r'[^"\\]+', String.Double),
            (r"\\.", String.Escape),
            (r'"', String.Double, "#pop"),
        ],
        "string_single": [
            (r"[^'\\]+", String.Single),
            (r"\\.", String.Escape),
            (r"'", String.Single, "#pop"),
        ],
    }
```

