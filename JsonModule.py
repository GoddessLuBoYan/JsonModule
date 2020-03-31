from enum import Enum

class JsonSerializer:
    @classmethod
    def dumps(cls, j):
        result = ''
        if type(j) == dict:
            result += '{'
            for i in j:
                result += cls.dumps(i) + ": " + cls.dumps(j[i]) + ", "
            if result.endswith(", "): 
                result = result[0:-2]
            result += '}'
        elif type(j) == list:
            result += '['
            for i in j:
                result += cls.dumps(i) + ", "
            if result.endswith(", "):
                result = result[0:-2]
            result += ']'
        elif type(j) == str:
            result = "\"" + j + "\""
        elif type(j) == int or type(j) == float:
            result = str(j)
        elif j == True:
            result = "true"
        elif j == False:
            result = "false"
        elif j == None:
            result = "null"
        else:
            raise Exception(j)
        return result
        
class TOKEN(Enum):
    INVALID = 0        # INVALID
    CURLY_OPEN = 1     # {
    CURLY_CLOSE = 2    # }
    SQUARED_OPEN = 3   # [
    SQUARED_CLOSE = 4  # ]
    COLON = 5          # :
    COMMA = 6          # ,
    STRING = 7         # "..."
    NUMBER = 8         # +-0.123456789
    TRUE = 9           # true
    FALSE = 10         # false
    NULL = 11          # null

class TokenReader:
    def __init__(self, token_list):
        self._id = 0
        self._token_list = token_list

    def next_token(self):
        token = self._token_list[self._id + 1]
        return token

    def read_token(self):
        token = self._token_list[self._id]
        self._id += 1
        return token

class JsonDeserializer:
    @classmethod
    def str2tokens(cls, string):
        curr = ""
        token_list = []
        reading_str = False
        for c in string:
            if reading_str:
                if c == '"':
                    reading_str = False
                    token_list.append((TOKEN.STRING, curr))
                    curr = ""
                else:
                    curr += c
            elif c in ' \t\r\n{}[]:,':
                if curr == "":
                    pass
                elif curr == 'true':
                    token_list.append((TOKEN.TRUE, True))
                    curr = ""
                elif curr == 'false':
                    token_list.append((TOKEN.FALSE, False))
                    curr = ""
                elif curr == 'null':
                    token_list.append((TOKEN.NULL, None))
                    curr = ""
                else:
                    try:
                        if '.' in curr:
                            num = float(curr)
                        else:
                            num = int(curr)
                    except Exception as e:
                        for token in token_list:
                            print(token)
                        raise Exception("failed to parse token {0}".format(curr))
                    token_list.append((TOKEN.NUMBER, num))
                    curr = ""
                if c == '{':
                    token_list.append((TOKEN.CURLY_OPEN, c))
                elif c == '}':
                    token_list.append((TOKEN.CURLY_CLOSE, c))
                elif c == '[':
                    token_list.append((TOKEN.SQUARED_OPEN, c))
                elif c == ']':
                    token_list.append((TOKEN.SQUARED_CLOSE, c))
                elif c == ':':
                    token_list.append((TOKEN.COLON, c))
                elif c == ',':
                    token_list.append((TOKEN.COMMA, c))
            elif c == '"':
                reading_str = True
            elif c in ' \t\r\n':
                pass
            else:
                curr += c
        curr = curr.strip()
        if curr:
            token_list.append((TOKEN.NONE, curr))
        return token_list

    @classmethod
    def tokenReader2json(cls, token_reader):
        result = None
        curr = token_reader.read_token()
        if curr[0] == TOKEN.CURLY_OPEN:
            result = result or {}
            next_token = token_reader.next_token()
            if next_token[0] == TOKEN.CURLY_CLOSE:
                token_reader.read_token()
                return result

            while True:
                curr = token_reader.read_token()
                assert curr[0] == TOKEN.STRING, curr
                key = curr[1]

                curr = token_reader.read_token()
                assert curr[0] == TOKEN.COLON, curr

                value = cls.tokenReader2json(token_reader)
                result[key] = value

                curr = token_reader.read_token()
                assert curr[0] in [TOKEN.CURLY_CLOSE, TOKEN.COMMA], curr

                if curr[0] == TOKEN.CURLY_CLOSE:
                    return result
        elif curr[0] == TOKEN.SQUARED_OPEN:
            result = result or []
            next_token = token_reader.next_token()
            if next_token[0] == TOKEN.SQUARED_CLOSE:
                token_reader.read_token()
                return result

            while True:

                value = cls.tokenReader2json(token_reader)
                result.append(value)

                curr = token_reader.read_token()
                assert curr[0] in [TOKEN.SQUARED_CLOSE, TOKEN.COMMA], curr

                if curr[0] == TOKEN.SQUARED_CLOSE:
                    return result
        elif curr[0] in [TOKEN.STRING, TOKEN.NUMBER, TOKEN.TRUE, TOKEN.FALSE, TOKEN.NULL]:
            return curr[1]
        elif curr[0] != TOKEN.INVALID:
            return None
        else:
            raise

    @classmethod
    def tokenList2json(cls, token_list):
        reader = TokenReader(token_list)
        return cls.tokenReader2json(reader)
    
    @classmethod
    def loads(cls, json_str):
        token_list = cls.str2tokens(json_str)
        return cls.tokenList2json(token_list)
        
class Json:
    @classmethod
    def dumps(cls, obj):
        return JsonSerializer.dumps(obj)
    
    @classmethod
    def loads(cls, json_str):
        return JsonDeserializer.loads(json_str)